import argparse
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


class DevError(RuntimeError):
    pass


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
    run: Callable[..., Any],
    grace_seconds: float,
) -> None:
    run(
        ["taskkill", "/PID", str(process.pid), "/T", "/F"],
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    if not _reap_process(process, grace_seconds):
        raise DevError(f"Could not reap Windows server process {process.pid}.")


def _stop_process(
    process: Any,
    *,
    platform_name: str = os.name,
    run: Callable[..., Any] = subprocess.run,
    grace_seconds: float = 5.0,
) -> None:
    if platform_name == "nt":
        _stop_process_windows(process, run, grace_seconds)
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
    output: TextIO = field(default_factory=lambda: sys.stdout)
    python_version: tuple[int, int, int] = field(
        default_factory=lambda: tuple(sys.version_info[:3])
    )
    platform_name: str = os.name


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


def doctor(services: Services) -> int:
    problems = []
    if services.python_version < (3, 11, 0):
        problems.append("Python 3.11 or newer is required.")

    node_version = _tool_version(services, ["node", "--version"])
    node_match = re.fullmatch(r"v?(\d+)(?:\.\d+){0,2}", node_version or "")
    if node_match is None or int(node_match.group(1)) < 20:
        problems.append("Node 20 or newer is required.")

    if _tool_version(services, ["npm", "--version"]) is None:
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
    _run_checked(services, ["npm", "ci"], cwd=services.root / "web" / "frontend")
    _print(services, "Development dependencies are installed.")
    return 0


def _run_package_checks(services: Services, python: str) -> None:
    root = services.root
    artifacts = sorted(path for path in (root / "dist").glob("*") if path.is_file())
    wheels = [path for path in artifacts if path.suffix == ".whl"]
    if not artifacts or not wheels:
        raise DevError("Package build did not produce both checkable artifacts and a wheel.")

    _run_checked(
        services,
        [python, "-m", "twine", "check", *(str(path) for path in artifacts)],
        cwd=root,
    )
    with services.temporary_directory() as temporary_root:
        isolated_venv = temporary_root / "wheel-venv"
        isolated_python = _venv_entrypoint(
            isolated_venv, "python", services.platform_name
        )
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
            executable = _venv_entrypoint(
                isolated_venv, entrypoint, services.platform_name
            )
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
        ([python, "-m", "build"], root),
    ]
    for argv, cwd in root_commands:
        _run_checked(services, argv, cwd=cwd)
    _run_package_checks(services, python)

    remaining_commands = [
        ([python, "-m", "ruff", "check", "."], backend),
        ([python, "-m", "pytest"], backend),
        (["npm", "run", "lint"], frontend),
        (["npm", "exec", "tsc", "--", "--noEmit"], frontend),
        (["npm", "run", "build"], frontend),
    ]
    for argv, cwd in remaining_commands:
        _run_checked(services, argv, cwd=cwd)
    _print(services, "All repository checks passed.")
    return 0


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
                "npm",
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
            process_group_options = {"creationflags": WINDOWS_NEW_PROCESS_GROUP}
        else:
            process_group_options = {"start_new_session": True}
        for argv, cwd in commands:
            processes.append(
                services.popen(
                    argv,
                    cwd=cwd,
                    env=environment,
                    shell=False,
                    **process_group_options,
                )
            )
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
