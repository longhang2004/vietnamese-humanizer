# Feature-gap implementation progress

Branch: `codex/wave1-foundation-containment`
Baseline: `70eea2c`
Scope: Wave 1 only; Vercel Analytics remains enabled without custom events.

| Task | Status | Commit | Review |
|---|---|---|---|
| W1-01 | Complete | `ddf730a` | Approved; no findings |
| W1-02 | Complete | `77cd41b`, `8423c79` | Approved after dependency-conflict fix |
| W1-03 | Complete | `dc2c357` | Approved; no findings |
| W1-04 | Complete | `a07f679`, `2d1a9c7` | Approved after metadata-contract fix |
| W1-05 | Complete | `81fe7c2`, `81c8733` | Approved after env-isolation fix |
| W1-06 | Complete | `44a7691` | Approved; no findings |
| W1-07 | Complete | `74a5c9d`, `2e30baa` | Approved after pre-body/Unicode fix |
| W1-08 | Complete | `eb61503`, `35df9b5` | Approved; two minor follow-up notes |
| W1-09 | Complete | `d652a9f`, `54a4ed2`, `8b30270`, `fc51fa1` | Approved after lifecycle hardening |
| W1-10 | Complete | `5a595db` | Approved; no findings |
| W1-11 | Complete | `fcb61de`, `b503272` | Approved after conduct/database docs fix |

## Review notes

- Minor: direct `/contribute` renders a blank main area while health is loading,
  disabled, or unavailable; consider an accessible unavailable/loading message.
- Minor: frontend capability contract tests are static substring checks and do
  not exercise malformed health, Strict Mode, UI flashes, or runtime lint
  independence.
- Minor: Win32 Job/Toolhelp ctypes behavior is adapter-tested but not yet run on
  native Windows CI.
- Minor: the port preflight-to-bind race is bounded but cannot be atomic across
  separately launched Uvicorn and Next processes.
- Minor: POSIX escalation is deterministically simulated rather than exercised
  with a live stubborn descendant.
