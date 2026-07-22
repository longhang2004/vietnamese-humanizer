import io
import json
import os
import signal
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

from vietnamese_writing_skills.cli import dev

ROOT = Path(__file__).resolve().parents[1]


def test_dev_script_exists_as_repository_entrypoint():
    assert (ROOT / "scripts" / "dev.py").is_file()


def test_dev_script_help_lists_all_commands():
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "dev.py"), "--help"],
        cwd=ROOT,
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
        if argv[0] == "npm" and argv[1:] == ["--version"]:
            return _completed("10.7.0\n")
        return _completed()

    return run


def _services(tmp_path, **overrides):
    values = {
        "root": tmp_path,
        "run": _tool_runner([]),
        "popen": lambda *args, **kwargs: None,
        "request": lambda *args, **kwargs: (200, b"{}"),
        "monotonic": lambda: 0.0,
        "sleep": lambda _seconds: None,
        "port_available": lambda _host, _port: True,
        "stop_process": lambda _process: None,
        "output": io.StringIO(),
        "python_version": (3, 13, 0),
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
    assert [call[0] for call in calls] == [["node", "--version"], ["npm", "--version"]]
    assert all(call[1]["shell"] is False for call in calls)
    assert ports == [("127.0.0.1", 8000), ("127.0.0.1", 3000)]
    assert "ready" in services.output.getvalue().lower()


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
    assert "Node 20" in report
    assert "npm" in report
    assert "3000" in report


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
    ]
    assert calls[2][0] == ["npm", "ci"]
    assert calls[2][1]["cwd"] == tmp_path / "web" / "frontend"
    assert all(call[1]["shell"] is False for call in calls)


def test_setup_reuses_an_existing_venv(tmp_path):
    venv_python = tmp_path / ".venv" / "bin" / "python"
    venv_python.parent.mkdir(parents=True)
    venv_python.touch()
    calls = []
    services = _services(tmp_path, run=_tool_runner(calls))

    assert dev.setup(services) == 0

    assert all(call[0][1:4] != ["-m", "venv", str(tmp_path / ".venv")] for call in calls)


def test_check_runs_core_backend_and_frontend_command_set(tmp_path):
    calls = []
    services = _services(tmp_path, run=_tool_runner(calls))

    assert dev.check(services) == 0

    commands = [call[0] for call in calls]
    assert [sys.executable, "-m", "ruff", "check", "."] in commands
    assert [sys.executable, "-m", "pytest"] in commands
    assert [sys.executable, "scripts/check_release_consistency.py"] in commands
    assert [sys.executable, "scripts/validate_skills.py"] in commands
    assert [sys.executable, "scripts/validate_patterns.py"] in commands
    assert [sys.executable, "scripts/validate_examples.py"] in commands
    assert [sys.executable, "scripts/run_benchmarks.py", "--validate-only"] in commands
    assert [sys.executable, "scripts/generate_pattern_docs.py", "--check"] in commands
    assert [sys.executable, "-m", "build"] in commands
    assert ["npm", "run", "lint"] in commands
    assert ["npm", "exec", "tsc", "--", "--noEmit"] in commands
    assert ["npm", "run", "build"] in commands
    backend_pytest = [
        call for call in calls if call[0] == [sys.executable, "-m", "pytest"]
    ]
    assert {call[1]["cwd"] for call in backend_pytest} == {
        tmp_path,
        tmp_path / "web" / "backend",
    }
    assert all(call[1]["shell"] is False for call in calls)


class FakeProcess:
    def __init__(self, pid):
        self.pid = pid

    def poll(self):
        return None


def test_stop_process_terminates_the_process_group_after_parent_exit(monkeypatch):
    signals = []
    process = FakeProcess(303)
    process.poll = lambda: 0
    monkeypatch.setattr(dev.os, "killpg", lambda pid, signum: signals.append((pid, signum)))

    dev._stop_process(process)

    assert signals == [(303, signal.SIGTERM)]


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
        "npm",
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
    assert stopped == [202, 101]


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
    assert any(call[0] == ["npm", "ci"] for call in calls)


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
