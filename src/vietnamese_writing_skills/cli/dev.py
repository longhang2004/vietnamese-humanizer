import argparse
import ctypes
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from collections.abc import Callable, Iterator
from contextlib import AbstractContextManager, contextmanager, suppress
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TextIO

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SERVER_HOST = "127.0.0.1"
PUBLIC_HOST = "localhost"
BACKEND_PORT = 8000
FRONTEND_PORT = 3000
SMOKE_TIMEOUT_SECONDS = 60.0
WINDOWS_NEW_PROCESS_GROUP = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200)
WINDOWS_CREATE_SUSPENDED = getattr(subprocess, "CREATE_SUSPENDED", 0x00000004)
_VENV_VERSION_CHECK = "import sys; raise SystemExit(sys.version_info < (3, 11))"
_PACKAGE_VERSION_CHECK = (
    "import pathlib, tomllib, vietnamese_writing_skills; "
    "expected = tomllib.loads(pathlib.Path('pyproject.toml').read_text())"
    "['project']['version']; "
    "assert vietnamese_writing_skills.__version__ == expected"
)
_PACKAGE_DATA_CHECK = (
    "from importlib.resources import files; "
    "root = files('vietnamese_writing_skills').joinpath('data'); "
    "assert root.joinpath('patterns/schema.json').is_file(); "
    "assert root.joinpath('examples/schema.json').is_file(); "
    "assert root.joinpath('benchmarks/case.schema.json').is_file(); "
    "assert root.joinpath('skills/humanizer-vi/SKILL.md').is_file()"
)
_NPM_UNRESOLVED = object()


class DevError(RuntimeError):
    pass


class _IoCounters(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_ulonglong),
        ("WriteOperationCount", ctypes.c_ulonglong),
        ("OtherOperationCount", ctypes.c_ulonglong),
        ("ReadTransferCount", ctypes.c_ulonglong),
        ("WriteTransferCount", ctypes.c_ulonglong),
        ("OtherTransferCount", ctypes.c_ulonglong),
    ]


class _BasicLimitInformation(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_longlong),
        ("PerJobUserTimeLimit", ctypes.c_longlong),
        ("LimitFlags", ctypes.c_uint32),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", ctypes.c_uint32),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", ctypes.c_uint32),
        ("SchedulingClass", ctypes.c_uint32),
    ]


class _ExtendedLimitInformation(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", _BasicLimitInformation),
        ("IoInfo", _IoCounters),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


class _ThreadEntry32(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_uint32),
        ("cntUsage", ctypes.c_uint32),
        ("th32ThreadID", ctypes.c_uint32),
        ("th32OwnerProcessID", ctypes.c_uint32),
        ("tpBasePri", ctypes.c_long),
        ("tpDeltaPri", ctypes.c_long),
        ("dwFlags", ctypes.c_uint32),
    ]


class _CtypesWindowsJobApi:
    _KILL_ON_JOB_CLOSE = 0x00002000
    _EXTENDED_LIMIT_INFORMATION_CLASS = 9

    def __init__(self) -> None:
        if os.name != "nt":
            raise DevError("Windows Job Objects are only available on Windows.")
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
        kernel32.CreateJobObjectW.restype = ctypes.c_void_p
        kernel32.SetInformationJobObject.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_void_p,
            ctypes.c_uint32,
        ]
        kernel32.SetInformationJobObject.restype = ctypes.c_int
        kernel32.AssignProcessToJobObject.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        kernel32.AssignProcessToJobObject.restype = ctypes.c_int
        kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
        kernel32.CloseHandle.restype = ctypes.c_int
        self.kernel32 = kernel32

    def _raise_last_error(self, action: str) -> None:
        error = ctypes.get_last_error()
        raise OSError(error, f"Could not {action} Windows Job Object")

    def create(self) -> int:
        handle = self.kernel32.CreateJobObjectW(None, None)
        if not handle:
            self._raise_last_error("create")
        return int(handle)

    def configure_kill_on_close(self, handle: int) -> None:
        information = _ExtendedLimitInformation()
        information.BasicLimitInformation.LimitFlags = self._KILL_ON_JOB_CLOSE
        configured = self.kernel32.SetInformationJobObject(
            handle,
            self._EXTENDED_LIMIT_INFORMATION_CLASS,
            ctypes.byref(information),
            ctypes.sizeof(information),
        )
        if not configured:
            self._raise_last_error("configure")

    def assign(self, handle: int, process_handle: int) -> None:
        if not self.kernel32.AssignProcessToJobObject(handle, process_handle):
            self._raise_last_error("assign process to")

    def close(self, handle: int) -> None:
        if not self.kernel32.CloseHandle(handle):
            self._raise_last_error("close")


class _CtypesWindowsThreadApi:
    _SNAP_THREADS = 0x00000004
    _THREAD_SUSPEND_RESUME = 0x0002
    _NO_MORE_FILES = 18
    _INVALID_HANDLE = ctypes.c_void_p(-1).value

    def __init__(self) -> None:
        if os.name != "nt":
            raise DevError("Windows thread APIs are only available on Windows.")
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateToolhelp32Snapshot.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
        kernel32.CreateToolhelp32Snapshot.restype = ctypes.c_void_p
        kernel32.Thread32First.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        kernel32.Thread32First.restype = ctypes.c_int
        kernel32.Thread32Next.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        kernel32.Thread32Next.restype = ctypes.c_int
        kernel32.OpenThread.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
        kernel32.OpenThread.restype = ctypes.c_void_p
        kernel32.ResumeThread.argtypes = [ctypes.c_void_p]
        kernel32.ResumeThread.restype = ctypes.c_uint32
        kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
        kernel32.CloseHandle.restype = ctypes.c_int
        self.kernel32 = kernel32

    def _raise_last_error(self, action: str) -> None:
        error = ctypes.get_last_error()
        raise OSError(error, f"Could not {action} Windows process thread")

    def thread_ids(self, process_id: int) -> list[int]:
        snapshot = self.kernel32.CreateToolhelp32Snapshot(self._SNAP_THREADS, 0)
        if snapshot == self._INVALID_HANDLE:
            self._raise_last_error("enumerate")
        entry = _ThreadEntry32()
        entry.dwSize = ctypes.sizeof(entry)
        thread_ids = []
        try:
            if not self.kernel32.Thread32First(snapshot, ctypes.byref(entry)):
                self._raise_last_error("read")
            while True:
                if entry.th32OwnerProcessID == process_id:
                    thread_ids.append(entry.th32ThreadID)
                if self.kernel32.Thread32Next(snapshot, ctypes.byref(entry)):
                    continue
                if ctypes.get_last_error() != self._NO_MORE_FILES:
                    self._raise_last_error("continue enumerating")
                return thread_ids
        finally:
            if not self.kernel32.CloseHandle(snapshot):
                self._raise_last_error("close thread snapshot for")

    def open_thread(self, thread_id: int) -> int:
        handle = self.kernel32.OpenThread(self._THREAD_SUSPEND_RESUME, False, thread_id)
        if not handle:
            self._raise_last_error("open")
        return int(handle)

    def resume_thread(self, handle: int) -> None:
        if self.kernel32.ResumeThread(handle) == 0xFFFFFFFF:
            self._raise_last_error("resume")

    def close(self, handle: int) -> None:
        if not self.kernel32.CloseHandle(handle):
            self._raise_last_error("close")


@dataclass
class WindowsJob:
    api: Any
    handle: int
    closed: bool = False

    def assign(self, process: Any) -> None:
        process_handle = getattr(process, "_handle", None)
        if process_handle is None:
            raise DevError("Could not assign process to Windows Job Object: missing handle.")
        try:
            self.api.assign(self.handle, process_handle)
        except OSError as exc:
            raise DevError(f"Could not assign process to Windows Job Object: {exc}") from exc

    def close(self) -> None:
        if self.closed:
            return
        last_error: OSError | None = None
        for _attempt in range(2):
            try:
                self.api.close(self.handle)
            except OSError as exc:
                last_error = exc
            else:
                self.closed = True
                return
        raise DevError(f"Could not close Windows Job Object: {last_error}") from last_error


def _create_windows_job(*, api: Any | None = None) -> WindowsJob:
    active_api = api or _CtypesWindowsJobApi()
    try:
        handle = active_api.create()
    except OSError as exc:
        raise DevError(f"Could not create Windows Job Object: {exc}") from exc
    job = WindowsJob(active_api, handle)
    try:
        active_api.configure_kill_on_close(handle)
    except OSError as exc:
        try:
            job.close()
        except DevError as close_exc:
            raise DevError(
                f"Could not configure or close Windows Job Object: {exc}; {close_exc}"
            ) from exc
        raise DevError(f"Could not configure Windows Job Object: {exc}") from exc
    return job


def _resume_windows_process(process: Any, *, api: Any | None = None) -> None:
    active_api = api or _CtypesWindowsThreadApi()
    try:
        thread_ids = active_api.thread_ids(process.pid)
    except OSError as exc:
        raise DevError(f"Could not enumerate suspended Windows process threads: {exc}") from exc
    if not thread_ids:
        raise DevError(f"Suspended Windows process {process.pid} has no resumable thread.")
    for thread_id in thread_ids:
        try:
            thread_handle = active_api.open_thread(thread_id)
        except OSError as exc:
            raise DevError(f"Could not open suspended Windows process thread: {exc}") from exc
        try:
            active_api.resume_thread(thread_handle)
        except OSError as exc:
            raise DevError(f"Could not resume suspended Windows process thread: {exc}") from exc
        finally:
            active_api.close(thread_handle)


def _register_process(processes: list[Any], process: Any) -> None:
    processes.append(process)


def _http_request(
    url: str,
    *,
    method: str = "GET",
    payload: bytes | None = None,
    timeout: float,
) -> tuple[int, bytes]:
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    request = urllib.request.Request(url, data=payload, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
        return response.status, response.read()


def _port_available(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as candidate:
        try:
            candidate.bind((host, port))
        except OSError:
            return False
    return True


def _group_is_extinct(process_group: int, deadline: float) -> bool:
    while True:
        try:
            os.killpg(process_group, 0)
        except ProcessLookupError:
            return True
        if time.monotonic() >= deadline:
            return False
        time.sleep(min(0.05, max(0.0, deadline - time.monotonic())))


def _reap_process(process: Any, timeout: float) -> bool:
    try:
        process.wait(timeout=max(0.0, timeout))
    except subprocess.TimeoutExpired:
        return False
    return True


def _stop_process_posix(process: Any, grace_seconds: float) -> None:
    deadline = time.monotonic() + grace_seconds
    with suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGTERM)

    leader_reaped = _reap_process(process, deadline - time.monotonic())
    group_extinct = _group_is_extinct(process.pid, deadline)
    if not group_extinct:
        with suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)
        kill_deadline = time.monotonic() + grace_seconds
        if not leader_reaped:
            leader_reaped = _reap_process(process, kill_deadline - time.monotonic())
        group_extinct = _group_is_extinct(process.pid, kill_deadline)

    if not leader_reaped:
        leader_reaped = _reap_process(process, grace_seconds)
    if not leader_reaped:
        raise DevError(f"Could not reap server process {process.pid}.")
    if not group_extinct:
        raise DevError(f"Could not stop server process group {process.pid}.")


def _stop_process_windows(
    process: Any,
    grace_seconds: float,
) -> None:
    job = getattr(process, "_dev_windows_job", None)
    close_error: Exception | None = None
    if job is None:
        close_error = DevError("Windows server process has no persistent Job Object.")
    else:
        try:
            job.close()
        except Exception as exc:
            close_error = exc

    if close_error is not None and process.poll() is None:
        with suppress(OSError):
            process.kill()
    leader_reaped = _reap_process(process, grace_seconds)
    if not leader_reaped:
        with suppress(OSError):
            process.kill()
        leader_reaped = _reap_process(process, grace_seconds)
    if not leader_reaped:
        raise DevError(f"Could not reap Windows server process {process.pid}.")
    if close_error is not None:
        raise DevError(f"Could not close Windows Job Object: {close_error}") from close_error


def _stop_process(
    process: Any,
    *,
    platform_name: str = os.name,
    grace_seconds: float = 5.0,
) -> None:
    if platform_name == "nt":
        _stop_process_windows(process, grace_seconds)
    else:
        _stop_process_posix(process, grace_seconds)


@contextmanager
def _temporary_directory() -> Iterator[Path]:
    with tempfile.TemporaryDirectory(prefix="viet-writing-package-") as directory:
        yield Path(directory)


@dataclass
class Services:
    root: Path = PROJECT_ROOT
    run: Callable[..., Any] = subprocess.run
    popen: Callable[..., Any] = subprocess.Popen
    request: Callable[..., tuple[int, bytes]] = _http_request
    monotonic: Callable[[], float] = time.monotonic
    sleep: Callable[[float], None] = time.sleep
    port_available: Callable[[str, int], bool] = _port_available
    stop_process: Callable[[Any], None] = _stop_process
    remove_tree: Callable[[Path], None] = shutil.rmtree
    temporary_directory: Callable[[], AbstractContextManager[Path]] = _temporary_directory
    windows_job_factory: Callable[[], WindowsJob] = _create_windows_job
    windows_resume_process: Callable[[Any], None] = _resume_windows_process
    register_process: Callable[[list[Any], Any], None] = _register_process
    which: Callable[[str], str | None] = shutil.which
    output: TextIO = field(default_factory=lambda: sys.stdout)
    python_version: tuple[int, int, int] = field(
        default_factory=lambda: tuple(sys.version_info[:3])
    )
    platform_name: str = os.name
    _npm_command: tuple[str, ...] | None | object = field(
        default=_NPM_UNRESOLVED,
        init=False,
        repr=False,
    )


def _print(services: Services, message: str) -> None:
    print(message, file=services.output, flush=True)


def _tool_version(services: Services, argv: list[str]) -> str | None:
    try:
        result = services.run(
            argv,
            cwd=services.root,
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
    except FileNotFoundError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _npm_argv(services: Services, *arguments: str) -> list[str]:
    if services._npm_command is _NPM_UNRESOLVED:
        npm_name = "npm.cmd" if services.platform_name == "nt" else "npm"
        npm_executable = services.which(npm_name)
        if npm_executable is None:
            services._npm_command = None
        elif services.platform_name == "nt":
            command_interpreter = services.which("cmd.exe")
            services._npm_command = (
                (
                    command_interpreter,
                    "/d",
                    "/s",
                    "/c",
                    "call",
                    npm_executable,
                )
                if command_interpreter is not None
                else None
            )
        else:
            services._npm_command = (npm_executable,)

    if services._npm_command is None:
        raise DevError("npm is required.")
    return [*services._npm_command, *arguments]


def doctor(services: Services) -> int:
    problems = []
    if services.python_version < (3, 11, 0):
        problems.append("Python 3.11 or newer is required.")

    node_version = _tool_version(services, ["node", "--version"])
    node_match = re.fullmatch(r"v?(\d+)(?:\.\d+){0,2}", node_version or "")
    if node_match is None or int(node_match.group(1)) < 20:
        problems.append("Node 20 or newer is required.")

    try:
        npm_version = _tool_version(services, _npm_argv(services, "--version"))
    except DevError:
        npm_version = None
    if npm_version is None:
        problems.append("npm is required.")

    for port in (BACKEND_PORT, FRONTEND_PORT):
        if not services.port_available(SERVER_HOST, port):
            problems.append(f"Port {port} is already in use.")

    if problems:
        for problem in problems:
            _print(services, f"[fail] {problem}")
        return 1
    _print(services, "Local prerequisites and ports are ready.")
    return 0


def _venv_python(root: Path, platform_name: str) -> Path:
    if platform_name == "nt":
        return root / ".venv" / "Scripts" / "python.exe"
    return root / ".venv" / "bin" / "python"


def _venv_entrypoint(venv: Path, name: str, platform_name: str) -> Path:
    if platform_name == "nt":
        return venv / "Scripts" / f"{name}.exe"
    return venv / "bin" / name


def _python_for(services: Services) -> str:
    venv_python = _venv_python(services.root, services.platform_name)
    return str(venv_python) if venv_python.is_file() else sys.executable


def _run_checked(services: Services, argv: list[str], *, cwd: Path) -> None:
    services.run(argv, cwd=cwd, check=True, shell=False)


def setup(services: Services) -> int:
    if services.python_version < (3, 11, 0):
        raise DevError("Python 3.11 or newer is required to create the development environment.")
    venv = services.root / ".venv"
    venv_python = _venv_python(services.root, services.platform_name)
    create_venv = not venv_python.is_file()
    if venv_python.is_file():
        try:
            version_check = services.run(
                [str(venv_python), "-c", _VENV_VERSION_CHECK],
                cwd=services.root,
                capture_output=True,
                text=True,
                check=False,
                shell=False,
            )
        except OSError:
            version_check = None
        if version_check is None or version_check.returncode != 0:
            services.remove_tree(venv)
            create_venv = True
    if create_venv:
        _run_checked(
            services,
            [sys.executable, "-m", "venv", str(services.root / ".venv")],
            cwd=services.root,
        )
    _run_checked(
        services,
        [
            str(venv_python),
            "-m",
            "pip",
            "install",
            "-e",
            ".[dev]",
            "-e",
            "web/backend[dev]",
            "twine>=5,<7",
        ],
        cwd=services.root,
    )
    _run_checked(services, _npm_argv(services, "ci"), cwd=services.root / "web" / "frontend")
    _print(services, "Development dependencies are installed.")
    return 0


def _run_package_checks(
    services: Services,
    python: str,
    artifacts_directory: Path,
    temporary_root: Path,
) -> None:
    root = services.root
    artifacts = sorted(path for path in artifacts_directory.iterdir() if path.is_file())
    wheels = [path for path in artifacts if path.suffix == ".whl"]
    if not artifacts or not wheels:
        raise DevError("Package build did not produce both checkable artifacts and a wheel.")

    _run_checked(
        services,
        [python, "-m", "twine", "check", *(str(path) for path in artifacts)],
        cwd=root,
    )
    isolated_venv = temporary_root / "wheel-venv"
    isolated_python = _venv_entrypoint(isolated_venv, "python", services.platform_name)
    _run_checked(
        services,
        [python, "-m", "venv", str(isolated_venv)],
        cwd=root,
    )
    _run_checked(
        services,
        [str(isolated_python), "-m", "pip", "install", *(str(path) for path in wheels)],
        cwd=root,
    )
    _run_checked(
        services,
        [str(isolated_python), "-c", _PACKAGE_VERSION_CHECK],
        cwd=root,
    )
    entrypoints = (
        "viet-writing-lint",
        "viet-writing-validate-skills",
        "viet-writing-validate-patterns",
        "viet-writing-validate-examples",
        "viet-writing-benchmark",
        "viet-writing-generate-docs",
    )
    for entrypoint in entrypoints:
        executable = _venv_entrypoint(isolated_venv, entrypoint, services.platform_name)
        _run_checked(services, [str(executable), "--help"], cwd=root)
    lint = _venv_entrypoint(isolated_venv, "viet-writing-lint", services.platform_name)
    _run_checked(
        services,
        [str(lint), "tests/fixtures/natural_article.md"],
        cwd=root,
    )
    _run_checked(
        services,
        [str(isolated_python), "-c", _PACKAGE_DATA_CHECK],
        cwd=root,
    )


def check(services: Services) -> int:
    python = _python_for(services)
    root = services.root
    frontend = root / "web" / "frontend"
    backend = root / "web" / "backend"
    root_commands = [
        ([python, "-m", "ruff", "check", "."], root),
        ([python, "-m", "pytest"], root),
        ([python, "scripts/check_release_consistency.py"], root),
        ([python, "scripts/validate_skills.py"], root),
        ([python, "scripts/validate_patterns.py"], root),
        ([python, "scripts/validate_examples.py"], root),
        ([python, "scripts/run_benchmarks.py", "--validate-only"], root),
        ([python, "scripts/generate_pattern_docs.py", "--check"], root),
    ]
    for argv, cwd in root_commands:
        _run_checked(services, argv, cwd=cwd)
    with services.temporary_directory() as package_root:
        artifacts_directory = package_root / "dist"
        _run_checked(
            services,
            [python, "-m", "build", "--outdir", str(artifacts_directory)],
            cwd=root,
        )
        _run_package_checks(
            services,
            python,
            artifacts_directory,
            package_root,
        )

    remaining_commands = [
        ([python, "-m", "ruff", "check", "."], backend),
        ([python, "-m", "pytest"], backend),
        (_npm_argv(services, "run", "lint"), frontend),
        (_npm_argv(services, "exec", "tsc", "--", "--noEmit"), frontend),
        (_npm_argv(services, "run", "build"), frontend),
    ]
    for argv, cwd in remaining_commands:
        _run_checked(services, argv, cwd=cwd)
    _print(services, "All repository checks passed.")
    return 0


def _discard_unmanaged_windows_child(process: Any, job: WindowsJob) -> None:
    close_error: Exception | None = None
    try:
        job.close()
    except Exception as exc:
        close_error = exc
    if process.poll() is None:
        with suppress(OSError):
            process.kill()
    reaped = _reap_process(process, 5.0)
    if not reaped:
        raise DevError(f"Could not reap unassigned Windows process {process.pid}.")
    if close_error is not None:
        raise DevError(f"Could not close unassigned Windows Job Object: {close_error}")


@contextmanager
def _defer_shutdown_signals() -> Iterator[None]:
    pending_signals = []
    previous_handlers = {}
    caught_error: BaseException | None = None

    def defer(signum: int, _frame: Any) -> None:
        pending_signals.append(signum)

    try:
        for signum in (signal.SIGINT, signal.SIGTERM):
            previous_handlers[signum] = signal.getsignal(signum)
            signal.signal(signum, defer)
        try:
            yield
        except BaseException as exc:
            caught_error = exc
    finally:
        for signum, handler in previous_handlers.items():
            signal.signal(signum, handler)
    if pending_signals:
        raise KeyboardInterrupt from caught_error
    if caught_error is not None:
        raise caught_error.with_traceback(caught_error.__traceback__)


def _cleanup_unregistered_process(
    services: Services,
    process: Any | None,
    windows_job: WindowsJob | None,
) -> None:
    if process is None:
        if windows_job is not None:
            windows_job.close()
        return
    if windows_job is not None:
        _discard_unmanaged_windows_child(process, windows_job)
    else:
        services.stop_process(process)


def _start_servers(services: Services) -> list[Any]:
    root = services.root
    environment = os.environ.copy()
    environment.update(
        {
            "REWRITE_ENABLED": "false",
            "CONTRIBUTIONS_ENABLED": "false",
            "ADMIN_API_ENABLED": "false",
            "FRONTEND_ORIGIN": f"http://{PUBLIC_HOST}:{FRONTEND_PORT}",
            "NEXT_PUBLIC_API_BASE_URL": f"http://{PUBLIC_HOST}:{BACKEND_PORT}",
        }
    )
    commands = [
        (
            [
                _python_for(services),
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                SERVER_HOST,
                "--port",
                str(BACKEND_PORT),
            ],
            root / "web" / "backend",
        ),
        (
            [
                *_npm_argv(services),
                "run",
                "dev",
                "--",
                "--hostname",
                SERVER_HOST,
                "--port",
                str(FRONTEND_PORT),
            ],
            root / "web" / "frontend",
        ),
    ]
    processes = []
    try:
        process_group_options: dict[str, Any]
        if services.platform_name == "nt":
            process_group_options = {
                "creationflags": WINDOWS_NEW_PROCESS_GROUP | WINDOWS_CREATE_SUSPENDED
            }
        else:
            process_group_options = {"start_new_session": True}
        for argv, cwd in commands:
            windows_job: WindowsJob | None = None
            process: Any | None = None
            registered = False
            try:
                with _defer_shutdown_signals():
                    if services.platform_name == "nt":
                        try:
                            windows_job = services.windows_job_factory()
                        except Exception as exc:
                            raise DevError(f"Could not create Windows Job Object: {exc}") from exc
                    process = services.popen(
                        argv,
                        cwd=cwd,
                        env=environment,
                        shell=False,
                        **process_group_options,
                    )
                    if windows_job is not None:
                        try:
                            windows_job.assign(process)
                        except Exception as exc:
                            raise DevError(f"Could not assign Windows Job Object: {exc}") from exc
                        process._dev_windows_job = windows_job
                    services.register_process(processes, process)
                    registered = True
                    if windows_job is not None:
                        services.windows_resume_process(process)
            except BaseException:
                if not registered:
                    try:
                        _cleanup_unregistered_process(services, process, windows_job)
                    except Exception as cleanup_exc:
                        _print(
                            services,
                            f"Warning: could not clean unregistered server process: {cleanup_exc}",
                        )
                raise
    except BaseException:
        _cleanup_servers(services, processes)
        raise
    return processes


def _cleanup_servers(services: Services, processes: list[Any]) -> None:
    for process in reversed(processes):
        try:
            services.stop_process(process)
        except Exception as exc:  # pragma: no cover - best effort after another failure
            _print(services, f"Warning: could not stop server process {process.pid}: {exc}")


def _remaining(services: Services, deadline: float) -> float:
    remaining = deadline - services.monotonic()
    if remaining <= 0:
        raise DevError("Timed out after 60 seconds waiting for the local demo.")
    return remaining


def _servers_running(processes: list[Any]) -> bool:
    return all(process.poll() is None for process in processes)


def _wait_for(
    services: Services,
    url: str,
    deadline: float,
    processes: list[Any],
    *,
    predicate: Callable[[int, bytes], bool],
) -> bytes:
    last_error: Exception | None = None
    while True:
        if not _servers_running(processes):
            raise DevError("A local server exited before becoming ready.")
        remaining = _remaining(services, deadline)
        try:
            status, body = services.request(url, timeout=remaining)
            if predicate(status, body):
                return body
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            last_error = exc
        remaining = _remaining(services, deadline)
        services.sleep(min(0.2, remaining))
        if last_error is not None and services.monotonic() >= deadline:
            raise DevError(f"Timed out waiting for {url}: {last_error}") from last_error


def _healthy(status: int, body: bytes) -> bool:
    if status != 200:
        return False
    data = json.loads(body)
    return isinstance(data, dict) and data.get("status") == "ok"


def _successful(status: int, _body: bytes) -> bool:
    return 200 <= status < 400


@contextmanager
def _shutdown_signals() -> Iterator[None]:
    previous = {}

    def stop(_signum: int, _frame: Any) -> None:
        raise KeyboardInterrupt

    try:
        for signum in (signal.SIGINT, signal.SIGTERM):
            previous[signum] = signal.getsignal(signum)
            signal.signal(signum, stop)
        yield
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)


def _prepare(services: Services, *, skip_setup: bool) -> bool:
    if doctor(services) != 0:
        return False
    if not skip_setup:
        setup(services)
    return True


def demo(services: Services, *, skip_setup: bool = False) -> int:
    if not _prepare(services, skip_setup=skip_setup):
        return 1
    processes = []
    try:
        with _shutdown_signals():
            processes = _start_servers(services)
            deadline = services.monotonic() + SMOKE_TIMEOUT_SECONDS
            _wait_for(
                services,
                f"http://{PUBLIC_HOST}:{BACKEND_PORT}/api/health",
                deadline,
                processes,
                predicate=_healthy,
            )
            _wait_for(
                services,
                f"http://{PUBLIC_HOST}:{FRONTEND_PORT}/",
                deadline,
                processes,
                predicate=_successful,
            )
            _print(
                services,
                f"Demo ready at http://{PUBLIC_HOST}:{FRONTEND_PORT}/ (Ctrl-C to stop).",
            )
            while _servers_running(processes):
                services.sleep(0.25)
            raise DevError("A local server exited unexpectedly.")
    except KeyboardInterrupt:
        _print(services, "Stopping local demo.")
        return 0
    except (DevError, OSError) as exc:
        _print(services, f"Demo failed: {exc}")
        return 1
    finally:
        _cleanup_servers(services, processes)


def smoke(services: Services, *, skip_setup: bool = False) -> int:
    if not _prepare(services, skip_setup=skip_setup):
        return 1
    processes = []
    try:
        with _shutdown_signals():
            processes = _start_servers(services)
            deadline = services.monotonic() + SMOKE_TIMEOUT_SECONDS
            _wait_for(
                services,
                f"http://{PUBLIC_HOST}:{BACKEND_PORT}/api/health",
                deadline,
                processes,
                predicate=_healthy,
            )
            _wait_for(
                services,
                f"http://{PUBLIC_HOST}:{FRONTEND_PORT}/",
                deadline,
                processes,
                predicate=_successful,
            )
            payload = json.dumps(
                {"text": "Trong bài viết này, chúng ta sẽ cùng tìm hiểu cách viết rõ hơn."}
            ).encode()
            status, body = services.request(
                f"http://{PUBLIC_HOST}:{BACKEND_PORT}/api/lint",
                method="POST",
                payload=payload,
                timeout=_remaining(services, deadline),
            )
            lint_result = json.loads(body)
            if (
                status != 200
                or not isinstance(lint_result, dict)
                or not isinstance(lint_result.get("issues"), list)
            ):
                raise DevError("Synthetic lint request returned an invalid response.")
            _print(services, "Smoke check passed: health, frontend, and synthetic lint are ready.")
            return 0
    except KeyboardInterrupt:
        _print(services, "Smoke check interrupted.")
        return 130
    except (DevError, OSError, ValueError, json.JSONDecodeError) as exc:
        _print(services, f"Smoke check failed: {exc}")
        return 1
    finally:
        _cleanup_servers(services, processes)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Develop and verify the local web application.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("doctor", help="Check Python, Node, npm, and local ports.")
    subparsers.add_parser("setup", help="Install Python and frontend dependencies.")
    for name, help_text in (
        ("demo", "Set up and run the local web application."),
        ("smoke", "Set up and smoke-test the local web application."),
    ):
        command = subparsers.add_parser(name, help=help_text)
        command.add_argument("--skip-setup", action="store_true")
    subparsers.add_parser("check", help="Run all repository checks.")
    return parser


def main(argv: list[str] | None = None, *, services: Services | None = None) -> int:
    args = build_parser().parse_args(argv)
    active_services = services or Services()
    try:
        if args.command == "doctor":
            return doctor(active_services)
        if args.command == "setup":
            return setup(active_services)
        if args.command == "demo":
            return demo(active_services, skip_setup=args.skip_setup)
        if args.command == "check":
            return check(active_services)
        if args.command == "smoke":
            return smoke(active_services, skip_setup=args.skip_setup)
    except (DevError, OSError, subprocess.SubprocessError) as exc:
        _print(active_services, f"{args.command} failed: {exc}")
        return 1
    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
