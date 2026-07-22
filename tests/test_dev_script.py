import io
import json
import os
import signal
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest

from vietnamese_writing_skills.cli import dev

ROOT = Path(__file__).resolve().parents[1]
POSIX_NPM = "/opt/node/bin/npm"
WINDOWS_NPM = r"C:\Program Files\nodejs\npm.cmd"
WINDOWS_COMMAND_INTERPRETER = r"C:\Windows\System32\cmd.exe"


def test_dev_script_exists_as_repository_entrypoint():
    assert (ROOT / "scripts" / "dev.py").is_file()


def test_dev_script_help_lists_all_commands_from_an_unrelated_cwd(tmp_path):
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "dev.py"), "--help"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
        shell=False,
        env=environment,
    )

    assert result.returncode == 0, result.stderr
    for command in ("doctor", "setup", "demo", "check", "smoke"):
        assert command in result.stdout


def _completed(stdout: str = ""):
    return SimpleNamespace(returncode=0, stdout=stdout, stderr="")


def _tool_runner(calls):
    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        if argv[0] == "node":
            return _completed("v20.15.0\n")
        if argv[0].endswith(("npm", "npm.cmd")) and argv[1:] == ["--version"]:
            return _completed("10.7.0\n")
        return _completed()

    return run


def _services(tmp_path, **overrides):
    @contextmanager
    def temporary_directory():
        path = tmp_path / "package-check"
        path.mkdir(exist_ok=True)
        yield path

    values = {
        "root": tmp_path,
        "run": _tool_runner([]),
        "popen": lambda *args, **kwargs: None,
        "request": lambda *args, **kwargs: (200, b"{}"),
        "monotonic": lambda: 0.0,
        "sleep": lambda _seconds: None,
        "port_available": lambda _host, _port: True,
        "stop_process": lambda _process: None,
        "remove_tree": lambda _path: None,
        "temporary_directory": temporary_directory,
        "windows_job_factory": lambda: None,
        "windows_resume_process": lambda _process: None,
        "register_process": lambda processes, process: processes.append(process),
        "which": lambda executable: {
            "npm": POSIX_NPM,
            "npm.cmd": WINDOWS_NPM,
            "cmd.exe": WINDOWS_COMMAND_INTERPRETER,
        }.get(executable),
        "output": io.StringIO(),
        "python_version": (3, 13, 0),
        "platform_name": "posix",
    }
    values.update(overrides)
    return dev.Services(**values)


def test_doctor_checks_versions_tools_and_both_ports_without_a_shell(tmp_path):
    calls = []
    ports = []
    services = _services(
        tmp_path,
        run=_tool_runner(calls),
        port_available=lambda host, port: ports.append((host, port)) or True,
    )

    assert dev.doctor(services) == 0
    assert [call[0] for call in calls] == [
        ["node", "--version"],
        [POSIX_NPM, "--version"],
    ]
    assert all(call[1]["shell"] is False for call in calls)
    assert ports == [("127.0.0.1", 8000), ("127.0.0.1", 3000)]
    assert "ready" in services.output.getvalue().lower()


def test_npm_command_resolves_absolute_posix_executable_once(tmp_path):
    resolutions = []
    services = _services(
        tmp_path,
        which=lambda executable: resolutions.append(executable) or POSIX_NPM,
    )

    assert dev._npm_argv(services, "--version") == [POSIX_NPM, "--version"]
    assert dev._npm_argv(services, "run", "lint") == [POSIX_NPM, "run", "lint"]
    assert resolutions == ["npm"]


def test_npm_command_uses_resolved_command_interpreter_for_windows_batch(tmp_path):
    resolutions = []

    def which(executable):
        resolutions.append(executable)
        return {
            "npm.cmd": WINDOWS_NPM,
            "cmd.exe": WINDOWS_COMMAND_INTERPRETER,
        }.get(executable)

    services = _services(tmp_path, platform_name="nt", which=which)

    assert dev._npm_argv(services, "run", "lint") == [
        WINDOWS_COMMAND_INTERPRETER,
        "/d",
        "/s",
        "/c",
        "call",
        WINDOWS_NPM,
        "run",
        "lint",
    ]
    assert dev._npm_argv(services, "ci")[-2:] == [WINDOWS_NPM, "ci"]
    assert resolutions == ["npm.cmd", "cmd.exe"]


def test_doctor_reports_missing_npm_without_attempting_provider_command(tmp_path):
    calls = []
    services = _services(
        tmp_path,
        run=_tool_runner(calls),
        which=lambda _executable: None,
    )

    assert dev.doctor(services) == 1
    assert [call[0] for call in calls] == [["node", "--version"]]
    assert "[fail] npm is required." in services.output.getvalue()


def test_doctor_reports_every_failed_prerequisite(tmp_path):
    def failed_tools(argv, **_kwargs):
        if argv[0] == "node":
            return SimpleNamespace(returncode=0, stdout="v19.9.0", stderr="")
        raise FileNotFoundError

    services = _services(
        tmp_path,
        run=failed_tools,
        port_available=lambda _host, port: port != 3000,
        python_version=(3, 10, 9),
    )

    assert dev.doctor(services) == 1
    report = services.output.getvalue()
    assert "Python 3.11" in report
    assert "Node 20.9" in report
    assert "npm" in report
    assert "3000" in report


def test_doctor_requires_node_20_9_or_newer(tmp_path):
    def old_node(argv, **_kwargs):
        if argv[0] == "node":
            return SimpleNamespace(returncode=0, stdout="v20.8.1", stderr="")
        return _completed()

    services = _services(tmp_path, run=old_node)

    assert dev.doctor(services) == 1
    assert "Node 20.9 or newer is required." in services.output.getvalue()


def test_setup_creates_venv_installs_both_editables_and_frontend(tmp_path):
    calls = []
    services = _services(tmp_path, run=_tool_runner(calls))

    assert dev.setup(services) == 0

    assert calls[0][0] == [sys.executable, "-m", "venv", str(tmp_path / ".venv")]
    assert calls[1][0] == [
        str(tmp_path / ".venv" / "bin" / "python"),
        "-m",
        "pip",
        "install",
        "-e",
        ".[dev]",
        "-e",
        "web/backend[dev]",
        "twine>=5,<7",
    ]
    assert calls[2][0] == [POSIX_NPM, "ci"]
    assert calls[2][1]["cwd"] == tmp_path / "web" / "frontend"
    assert all(call[1]["shell"] is False for call in calls)


def test_setup_rejects_python_310_before_touching_the_environment(tmp_path):
    calls = []
    services = _services(tmp_path, run=_tool_runner(calls), python_version=(3, 10, 14))

    with pytest.raises(dev.DevError, match="Python 3.11"):
        dev.setup(services)

    assert calls == []


def test_setup_reuses_an_existing_venv(tmp_path):
    venv_python = tmp_path / ".venv" / "bin" / "python"
    venv_python.parent.mkdir(parents=True)
    venv_python.touch()
    calls = []
    services = _services(tmp_path, run=_tool_runner(calls))

    assert dev.setup(services) == 0

    assert calls[0][0] == [
        str(venv_python),
        "-c",
        "import sys; raise SystemExit(sys.version_info < (3, 11))",
    ]
    assert all(call[0][1:4] != ["-m", "venv", str(tmp_path / ".venv")] for call in calls)


def test_setup_recreates_an_existing_python_310_venv(tmp_path):
    venv_python = tmp_path / ".venv" / "bin" / "python"
    venv_python.parent.mkdir(parents=True)
    venv_python.touch()
    calls = []
    removed = []

    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        if argv[:2] == [str(venv_python), "-c"]:
            return SimpleNamespace(returncode=1, stdout="", stderr="")
        return _completed()

    services = _services(
        tmp_path,
        run=run,
        remove_tree=lambda path: removed.append(path),
    )

    assert dev.setup(services) == 0
    assert removed == [tmp_path / ".venv"]
    assert [sys.executable, "-m", "venv", str(tmp_path / ".venv")] in [
        call[0] for call in calls
    ]


def test_venv_executables_are_platform_aware(tmp_path):
    assert dev._venv_python(tmp_path, "posix") == tmp_path / ".venv" / "bin" / "python"
    assert dev._venv_python(tmp_path, "nt") == tmp_path / ".venv" / "Scripts" / "python.exe"
    assert dev._venv_entrypoint(tmp_path / "wheel", "viet-writing-lint", "nt") == (
        tmp_path / "wheel" / "Scripts" / "viet-writing-lint.exe"
    )


def test_check_runs_core_backend_and_frontend_command_set(tmp_path):
    calls = []

    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        if argv[:3] == [sys.executable, "-m", "build"]:
            output = Path(argv[-1])
            output.mkdir(parents=True)
            (output / "package.whl").touch()
            (output / "package.tar.gz").touch()
        return _completed()

    services = _services(tmp_path, run=run)

    assert dev.check(services) == 0

    commands = [call[0] for call in calls]
    package_root = tmp_path / "package-check"
    dist = package_root / "dist"
    wheel = dist / "package.whl"
    source = dist / "package.tar.gz"
    assert commands[:8] == [
        [sys.executable, "-m", "ruff", "check", "."],
        [sys.executable, "-m", "pytest"],
        [sys.executable, "scripts/check_release_consistency.py"],
        [sys.executable, "scripts/validate_skills.py"],
        [sys.executable, "scripts/validate_patterns.py"],
        [sys.executable, "scripts/validate_examples.py"],
        [sys.executable, "scripts/run_benchmarks.py", "--validate-only"],
        [sys.executable, "scripts/generate_pattern_docs.py", "--check"],
    ]
    assert commands[8] == [sys.executable, "-m", "build", "--outdir", str(dist)]
    assert commands[9] == [sys.executable, "-m", "twine", "check", str(source), str(wheel)]
    isolated = package_root / "wheel-venv"
    isolated_python = isolated / "bin" / "python"
    assert commands[10] == [sys.executable, "-m", "venv", str(isolated)]
    assert commands[11] == [str(isolated_python), "-m", "pip", "install", str(wheel)]
    assert commands[12][:2] == [str(isolated_python), "-c"]
    assert "__version__" in commands[12][2]
    expected_entrypoints = [
        "viet-writing-lint",
        "viet-writing-validate-skills",
        "viet-writing-validate-patterns",
        "viet-writing-validate-examples",
        "viet-writing-benchmark",
        "viet-writing-generate-docs",
    ]
    assert commands[13:19] == [
        [str(isolated / "bin" / entrypoint), "--help"] for entrypoint in expected_entrypoints
    ]
    assert commands[19] == [
        str(isolated / "bin" / "viet-writing-lint"),
        "tests/fixtures/natural_article.md",
    ]
    assert commands[20][:2] == [str(isolated_python), "-c"]
    assert "patterns/schema.json" in commands[20][2]
    assert commands[21:] == [
        [sys.executable, "-m", "ruff", "check", "."],
        [sys.executable, "-m", "pytest"],
        [POSIX_NPM, "run", "lint"],
        [POSIX_NPM, "exec", "tsc", "--", "--noEmit"],
        [POSIX_NPM, "run", "build"],
    ]
    assert [call[1]["cwd"] for call in calls[:21]] == [tmp_path] * 21
    assert [call[1]["cwd"] for call in calls[21:23]] == [
        tmp_path / "web" / "backend"
    ] * 2
    assert [call[1]["cwd"] for call in calls[23:]] == [
        tmp_path / "web" / "frontend"
    ] * 3
    assert all(call[1]["shell"] is False for call in calls)


class FakeProcess:
    def __init__(self, pid):
        self.pid = pid
        self.wait_calls = []

    def poll(self):
        return None

    def wait(self, timeout):
        self.wait_calls.append(timeout)
        return 0

    def kill(self):
        self.kill_calls = getattr(self, "kill_calls", 0) + 1


def test_stop_process_reaps_leader_and_confirms_posix_group_extinction(monkeypatch):
    signals = []
    process = FakeProcess(303)
    process.poll = lambda: 0

    def kill_group(pid, signum):
        signals.append((pid, signum))
        if signum == 0:
            raise ProcessLookupError

    monkeypatch.setattr(dev.os, "killpg", kill_group)

    dev._stop_process(process, platform_name="posix", grace_seconds=0)

    assert signals == [(303, signal.SIGTERM), (303, 0)]
    assert len(process.wait_calls) == 1


def test_stop_process_escalates_until_posix_group_is_extinct(monkeypatch):
    process = FakeProcess(404)

    def wait(timeout):
        process.wait_calls.append(timeout)
        if len(process.wait_calls) == 1:
            raise subprocess.TimeoutExpired("server", timeout)
        return 0

    process.wait = wait
    sent = []
    probes = iter([True, True, False])
    clock = Clock()

    def kill_group(pid, signum):
        if signum == 0:
            if next(probes):
                return
            raise ProcessLookupError
        sent.append((pid, signum))

    monkeypatch.setattr(dev.os, "killpg", kill_group)
    monkeypatch.setattr(dev.time, "monotonic", clock.monotonic)
    monkeypatch.setattr(dev.time, "sleep", clock.sleep)

    dev._stop_process(process, platform_name="posix", grace_seconds=1)

    assert sent == [(404, signal.SIGTERM), (404, signal.SIGKILL)]
    assert len(process.wait_calls) == 2


class FakeWindowsJob:
    def __init__(self, *, assign_error=None, close_error=None):
        self.assign_error = assign_error
        self.close_error = close_error
        self.assigned = []
        self.close_calls = 0

    def assign(self, process):
        self.assigned.append(process.pid)
        if self.assign_error:
            raise self.assign_error

    def close(self):
        self.close_calls += 1
        if self.close_error:
            raise self.close_error


class FakeWindowsJobApi:
    def __init__(
        self,
        *,
        create_error=None,
        configure_error=None,
        assign_error=None,
        close_failures=0,
    ):
        self.create_error = create_error
        self.configure_error = configure_error
        self.assign_error = assign_error
        self.close_failures = close_failures
        self.calls = []

    def create(self):
        self.calls.append(("create",))
        if self.create_error:
            raise self.create_error
        return 91

    def configure_kill_on_close(self, handle):
        self.calls.append(("configure", handle))
        if self.configure_error:
            raise self.configure_error

    def assign(self, handle, process_handle):
        self.calls.append(("assign", handle, process_handle))
        if self.assign_error:
            raise self.assign_error

    def close(self, handle):
        self.calls.append(("close", handle))
        if self.close_failures:
            self.close_failures -= 1
            raise OSError("close failed")


def test_windows_job_is_configured_assigned_and_closed_without_leaking():
    api = FakeWindowsJobApi()
    process = FakeProcess(505)
    process._handle = 1234

    job = dev._create_windows_job(api=api)
    job.assign(process)
    job.close()
    job.close()

    assert api.calls == [
        ("create",),
        ("configure", 91),
        ("assign", 91, 1234),
        ("close", 91),
    ]


def test_windows_job_configuration_failure_closes_the_handle():
    api = FakeWindowsJobApi(configure_error=OSError("configure failed"))

    with pytest.raises(dev.DevError, match="configure"):
        dev._create_windows_job(api=api)

    assert api.calls == [("create",), ("configure", 91), ("close", 91)]


def test_windows_job_creation_failure_has_no_handle_to_leak():
    api = FakeWindowsJobApi(create_error=OSError("create failed"))

    with pytest.raises(dev.DevError, match="create"):
        dev._create_windows_job(api=api)

    assert api.calls == [("create",)]


def test_windows_job_configuration_failure_retries_handle_close():
    api = FakeWindowsJobApi(
        configure_error=OSError("configure failed"),
        close_failures=1,
    )

    with pytest.raises(dev.DevError, match="configure"):
        dev._create_windows_job(api=api)

    assert api.calls[-2:] == [("close", 91), ("close", 91)]


def test_windows_job_retries_a_transient_close_failure_without_leaking():
    api = FakeWindowsJobApi(close_failures=1)
    job = dev._create_windows_job(api=api)

    job.close()

    assert api.calls[-2:] == [("close", 91), ("close", 91)]


def test_stop_process_closes_persistent_windows_job_after_leader_exit():
    process = FakeProcess(505)
    process.poll = lambda: 0
    job = FakeWindowsJob()
    process._dev_windows_job = job

    dev._stop_process(process, platform_name="nt")

    assert job.close_calls == 1
    assert len(process.wait_calls) == 1


def test_stop_process_reaps_windows_leader_when_job_close_fails():
    process = FakeProcess(506)
    process._dev_windows_job = FakeWindowsJob(close_error=OSError("close failed"))

    with pytest.raises(dev.DevError, match="close"):
        dev._stop_process(process, platform_name="nt")

    assert len(process.wait_calls) == 1


def _server_services(tmp_path, *, request, sleep=lambda _seconds: None, monotonic=lambda: 0):
    processes = [FakeProcess(101), FakeProcess(202)]
    popen_calls = []
    stopped = []

    def popen(argv, **kwargs):
        popen_calls.append((argv, kwargs))
        return processes[len(popen_calls) - 1]

    services = _services(
        tmp_path,
        popen=popen,
        request=request,
        sleep=sleep,
        monotonic=monotonic,
        stop_process=lambda process: stopped.append(process.pid),
    )
    return services, popen_calls, stopped


def test_demo_starts_with_argv_lists_and_cleans_up_both_servers_on_interrupt(tmp_path):
    def request(url, **_kwargs):
        if url.endswith("/api/health"):
            return 200, json.dumps({"status": "ok"}).encode()
        return 200, b"<!doctype html>"

    def interrupt(_seconds):
        raise KeyboardInterrupt

    services, popen_calls, stopped = _server_services(
        tmp_path, request=request, sleep=interrupt
    )

    assert dev.demo(services, skip_setup=True) == 0
    assert popen_calls[0][0] == [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
    ]
    assert popen_calls[1][0] == [
        POSIX_NPM,
        "run",
        "dev",
        "--",
        "--hostname",
        "127.0.0.1",
        "--port",
        "3000",
    ]
    assert all(call[1]["shell"] is False for call in popen_calls)
    assert all(call[1]["start_new_session"] is True for call in popen_calls)
    assert popen_calls[0][1]["env"]["FRONTEND_ORIGIN"] == "http://localhost:3000"
    assert popen_calls[1][1]["env"]["NEXT_PUBLIC_API_BASE_URL"] == "http://localhost:8000"
    assert "http://localhost:3000" in services.output.getvalue()
    assert stopped == [202, 101]


def test_windows_servers_use_new_process_groups_without_start_new_session(tmp_path):
    def request(url, **_kwargs):
        if url.endswith("/api/health"):
            return 200, b'{"status":"ok"}'
        return 200, b"home"

    services, popen_calls, _stopped = _server_services(
        tmp_path, request=request, sleep=lambda _seconds: (_ for _ in ()).throw(KeyboardInterrupt)
    )
    services.platform_name = "nt"
    jobs = [FakeWindowsJob(), FakeWindowsJob()]
    pending_jobs = iter(jobs)
    services.windows_job_factory = lambda: next(pending_jobs)

    assert dev.demo(services, skip_setup=True) == 0
    assert all("start_new_session" not in call[1] for call in popen_calls)
    assert all(
        call[1]["creationflags"]
        == dev.WINDOWS_NEW_PROCESS_GROUP | dev.WINDOWS_CREATE_SUSPENDED
        for call in popen_calls
    )
    assert popen_calls[1][0] == [
        WINDOWS_COMMAND_INTERPRETER,
        "/d",
        "/s",
        "/c",
        "call",
        WINDOWS_NPM,
        "run",
        "dev",
        "--",
        "--hostname",
        "127.0.0.1",
        "--port",
        "3000",
    ]
    assert all(call[1]["shell"] is False for call in popen_calls)
    assert [job.assigned for job in jobs] == [[101], [202]]


def test_windows_assignment_failure_closes_job_kills_and_reaps_child(tmp_path):
    process = FakeProcess(606)
    job = FakeWindowsJob(assign_error=OSError("assign failed"))
    services = _services(
        tmp_path,
        platform_name="nt",
        popen=lambda *_args, **_kwargs: process,
        windows_job_factory=lambda: job,
    )

    with pytest.raises(dev.DevError, match="assign"):
        dev._start_servers(services)

    assert job.close_calls == 1
    assert process.kill_calls == 1
    assert len(process.wait_calls) == 1


def test_windows_job_creation_failure_does_not_start_a_child(tmp_path):
    popen_calls = []
    services = _services(
        tmp_path,
        platform_name="nt",
        popen=lambda *_args, **_kwargs: popen_calls.append(True),
        windows_job_factory=lambda: (_ for _ in ()).throw(OSError("create failed")),
    )

    with pytest.raises(dev.DevError, match="create"):
        dev._start_servers(services)

    assert popen_calls == []


def test_windows_popen_failure_after_job_creation_closes_handle(tmp_path):
    job = FakeWindowsJob()
    services = _services(
        tmp_path,
        platform_name="nt",
        windows_job_factory=lambda: job,
        popen=lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("spawn failed")),
    )

    with pytest.raises(OSError, match="spawn failed"):
        dev._start_servers(services)

    assert job.close_calls == 1


def test_windows_second_child_failure_cleans_first_child_and_current_job(tmp_path):
    first_process = FakeProcess(701)
    jobs = [FakeWindowsJob(), FakeWindowsJob()]
    pending_jobs = iter(jobs)
    popen_calls = 0
    stopped = []

    def popen(*_args, **_kwargs):
        nonlocal popen_calls
        popen_calls += 1
        if popen_calls == 2:
            raise OSError("second spawn failed")
        return first_process

    def stop(process):
        stopped.append(process.pid)
        process._dev_windows_job.close()

    services = _services(
        tmp_path,
        platform_name="nt",
        windows_job_factory=lambda: next(pending_jobs),
        popen=popen,
        stop_process=stop,
    )

    with pytest.raises(OSError, match="second spawn failed"):
        dev._start_servers(services)

    assert stopped == [701]
    assert [job.close_calls for job in jobs] == [1, 1]


def test_windows_keyboard_interrupt_during_assignment_cleans_current_child_and_job(tmp_path):
    process = FakeProcess(702)
    job = FakeWindowsJob(assign_error=KeyboardInterrupt())
    services = _services(
        tmp_path,
        platform_name="nt",
        windows_job_factory=lambda: job,
        popen=lambda *_args, **_kwargs: process,
    )

    with pytest.raises(KeyboardInterrupt):
        dev._start_servers(services)

    assert job.close_calls == 1
    assert process.kill_calls == 1
    assert len(process.wait_calls) == 1


def test_windows_child_is_suspended_assigned_registered_then_resumed(tmp_path):
    events = []
    process = FakeProcess(703)

    class OrderedJob(FakeWindowsJob):
        def assign(self, assigned_process):
            events.append("assign")
            super().assign(assigned_process)

    job = OrderedJob()

    def popen(_argv, **kwargs):
        assert kwargs["creationflags"] & dev.WINDOWS_CREATE_SUSPENDED
        events.append("popen")
        return process

    def register(processes, registered_process):
        events.append("register")
        processes.append(registered_process)

    services = _services(
        tmp_path,
        platform_name="nt",
        windows_job_factory=lambda: job,
        windows_resume_process=lambda _process: events.append("resume"),
        register_process=register,
        popen=popen,
    )

    processes = dev._start_servers(services)

    assert events[:4] == ["popen", "assign", "register", "resume"]
    assert processes[0] is process
    dev._cleanup_servers(services, processes)


def test_windows_resume_interrupt_is_cleaned_from_registered_children(tmp_path):
    process = FakeProcess(707)
    stopped = []
    services = _services(
        tmp_path,
        platform_name="nt",
        windows_job_factory=FakeWindowsJob,
        windows_resume_process=lambda _process: (_ for _ in ()).throw(
            KeyboardInterrupt()
        ),
        popen=lambda *_args, **_kwargs: process,
        stop_process=lambda current: stopped.append(current.pid),
    )

    with pytest.raises(KeyboardInterrupt):
        dev._start_servers(services)

    assert stopped == [707]


def test_windows_resume_helper_closes_every_opened_thread_handle():
    events = []

    class ThreadApi:
        def thread_ids(self, pid):
            events.append(("enumerate", pid))
            return [11, 12]

        def open_thread(self, thread_id):
            events.append(("open", thread_id))
            return thread_id + 100

        def resume_thread(self, handle):
            events.append(("resume", handle))

        def close(self, handle):
            events.append(("close", handle))

    dev._resume_windows_process(FakeProcess(704), api=ThreadApi())

    assert events == [
        ("enumerate", 704),
        ("open", 11),
        ("resume", 111),
        ("close", 111),
        ("open", 12),
        ("resume", 112),
        ("close", 112),
    ]


def test_posix_registration_baseexception_cleans_returned_child(tmp_path):
    process = FakeProcess(705)
    stopped = []
    services = _services(
        tmp_path,
        popen=lambda *_args, **_kwargs: process,
        register_process=lambda _processes, _process: (_ for _ in ()).throw(
            KeyboardInterrupt()
        ),
        stop_process=lambda current: stopped.append(current.pid),
    )

    with pytest.raises(KeyboardInterrupt):
        dev._start_servers(services)

    assert stopped == [705]


def test_deferred_interrupt_is_preserved_when_registration_also_fails(tmp_path):
    process = FakeProcess(706)
    stopped = []

    def interrupted_registration(_processes, _process):
        signal.raise_signal(signal.SIGINT)
        raise OSError("registration failed after interrupt")

    services = _services(
        tmp_path,
        popen=lambda *_args, **_kwargs: process,
        register_process=interrupted_registration,
        stop_process=lambda current: stopped.append(current.pid),
    )

    with pytest.raises(KeyboardInterrupt):
        dev._start_servers(services)

    assert stopped == [706]


def test_demo_installs_signal_cleanup_before_starting_children(tmp_path, monkeypatch):
    signal_cleanup_active = False

    @contextmanager
    def signal_cleanup():
        nonlocal signal_cleanup_active
        signal_cleanup_active = True
        try:
            yield
        finally:
            signal_cleanup_active = False

    def request(url, **_kwargs):
        if url.endswith("/api/health"):
            return 200, b'{"status":"ok"}'
        return 200, b"home"

    services, _popen_calls, _stopped = _server_services(
        tmp_path, request=request, sleep=lambda _seconds: (_ for _ in ()).throw(KeyboardInterrupt)
    )
    original_popen = services.popen

    def popen(*args, **kwargs):
        assert signal_cleanup_active
        return original_popen(*args, **kwargs)

    services.popen = popen
    monkeypatch.setattr(dev, "_shutdown_signals", signal_cleanup)

    assert dev.demo(services, skip_setup=True) == 0


def test_demo_runs_setup_by_default(tmp_path):
    calls = []

    def request(url, **_kwargs):
        if url.endswith("/api/health"):
            return 200, b'{"status":"ok"}'
        return 200, b"home"

    services, _popen_calls, _stopped = _server_services(
        tmp_path, request=request, sleep=lambda _seconds: (_ for _ in ()).throw(KeyboardInterrupt)
    )
    services.run = _tool_runner(calls)

    assert dev.demo(services) == 0
    assert any(call[0][1:3] == ["-m", "venv"] for call in calls)
    assert any(call[0] == [POSIX_NPM, "ci"] for call in calls)


class Clock:
    def __init__(self):
        self.now = 0.0

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.now += max(seconds, 10.0)


def test_smoke_uses_one_60_second_deadline_and_posts_synthetic_lint(tmp_path):
    clock = Clock()
    requests = []

    def request(url, *, method="GET", payload=None, timeout):
        requests.append((url, method, payload, timeout))
        clock.now += 10
        if url.endswith("/api/health"):
            return 200, b'{"status":"ok"}'
        if url.endswith("/api/lint"):
            return 200, b'{"summary":{"total":0},"issues":[]}'
        return 200, b"home"

    services, _popen_calls, stopped = _server_services(
        tmp_path, request=request, monotonic=clock.monotonic, sleep=clock.sleep
    )

    assert dev.smoke(services, skip_setup=True) == 0
    assert [request[3] for request in requests] == [60.0, 50.0, 40.0]
    lint_request = requests[-1]
    assert lint_request[1] == "POST"
    assert json.loads(lint_request[2])["text"]
    assert stopped == [202, 101]


def test_smoke_times_out_within_shared_budget_and_still_cleans_up(tmp_path):
    clock = Clock()
    timeouts = []

    def unavailable(_url, *, timeout, **_kwargs):
        timeouts.append(timeout)
        raise OSError("not ready")

    services, _popen_calls, stopped = _server_services(
        tmp_path, request=unavailable, monotonic=clock.monotonic, sleep=clock.sleep
    )

    assert dev.smoke(services, skip_setup=True) == 1
    assert max(timeouts) <= 60
    assert clock.now == 60
    assert stopped == [202, 101]


def test_smoke_rejects_a_malformed_lint_response_and_cleans_up(tmp_path):
    def request(url, **_kwargs):
        if url.endswith("/api/health"):
            return 200, b'{"status":"ok"}'
        if url.endswith("/api/lint"):
            return 200, b"[]"
        return 200, b"home"

    services, _popen_calls, stopped = _server_services(tmp_path, request=request)

    assert dev.smoke(services, skip_setup=True) == 1
    assert stopped == [202, 101]
