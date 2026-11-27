"use client";

import { useCallback, useEffect, useId, useRef, useState } from "react";
import { starterSkills } from "../lib/onboarding";
import { Icon } from "./Icon";

const BASE_INSTALL_COMMAND = "npx skills add longhang2004/vietnamese-humanizer";
const FEEDBACK_TIMEOUT_MS = 2200;

// Track the last announced message page-wide so VoiceOver still reads
// repeated identical outcomes instead of eliding them.
let lastAnnouncedMessage = "";

export function resetLastAnnouncedMessageForTests(): void {
  lastAnnouncedMessage = "";
}

export function buildInstallCommand(skillId: string): string {
  if (!skillId || skillId === "all") {
    return BASE_INSTALL_COMMAND;
  }
  return `${BASE_INSTALL_COMMAND} --skill ${skillId}`;
}

export interface InstallCommandProps {
  variant?: "default" | "hero";
  label?: string;
  allowSkillSelect?: boolean;
}

type CopyStatus = "idle" | "copied" | "failed";

export function InstallCommand({
  variant = "default",
  label,
  allowSkillSelect = false,
}: InstallCommandProps) {
  const codeId = useId();
  const selectId = useId();
  const codeRef = useRef<HTMLElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const timerRef = useRef<number | null>(null);

  const [selectedSkill, setSelectedSkill] = useState("all");
  const [status, setStatus] = useState<CopyStatus>("idle");
  const [statusMessage, setStatusMessage] = useState("");

  const command = buildInstallCommand(selectedSkill);

  const clearFeedback = useCallback(() => {
    if (timerRef.current !== null) {
      window.clearTimeout(timerRef.current);
      timerRef.current = null;
    }
    setStatus("idle");
    setStatusMessage("");
  }, []);

  const report = useCallback((ok: boolean) => {
    if (timerRef.current !== null) {
      window.clearTimeout(timerRef.current);
      timerRef.current = null;
    }

    let message = ok ? "Đã sao chép" : "Chưa sao chép được";
    if (message === lastAnnouncedMessage) {
      message += "\u00A0";
    }
    lastAnnouncedMessage = message;

    setStatus(ok ? "copied" : "failed");
    setStatusMessage(message);

    timerRef.current = window.setTimeout(() => {
      timerRef.current = null;
      setStatus("idle");
      setStatusMessage("");
    }, FEEDBACK_TIMEOUT_MS);
  }, []);

  const copyCommand = useCallback(async () => {
    const codeEl = codeRef.current;
    if (!codeEl) return;
    const text = (codeEl.innerText ?? codeEl.textContent ?? "").trim();
    if (!text) return;

    try {
      await navigator.clipboard.writeText(text);
      report(true);
    } catch {
      report(false);
    }
  }, [report]);

  useEffect(() => {
    const codeEl = codeRef.current;
    const buttonEl = buttonRef.current;
    if (!codeEl || !buttonEl) return;

    if ("CommandEvent" in window) {
      const handleCommand = (event: Event) => {
        const commandName = (event as Event & { command?: string }).command;
        if (commandName === "--copy") {
          void copyCommand();
        }
      };
      codeEl.addEventListener("command", handleCommand);
      return () => {
        codeEl.removeEventListener("command", handleCommand);
      };
    }

    const handleClick = (event: MouseEvent) => {
      if (event.defaultPrevented) return;
      void copyCommand();
    };
    buttonEl.addEventListener("click", handleClick);
    return () => {
      buttonEl.removeEventListener("click", handleClick);
    };
  }, [copyCommand]);

  useEffect(() => {
    return () => {
      if (timerRef.current !== null) {
        window.clearTimeout(timerRef.current);
      }
    };
  }, []);

  function handleSkillChange(nextSkill: string) {
    setSelectedSkill(nextSkill);
    clearFeedback();
  }

  const accessibleTarget =
    selectedSkill === "all"
      ? "lệnh cài tất cả 4 skill"
      : `lệnh cài skill ${selectedSkill}`;

  const invokerProps = {
    command: "--copy",
    commandfor: codeId,
  } as Record<string, string>;

  const headingLabel = label ?? (allowSkillSelect ? "Chọn phạm vi cài" : null);

  return (
    <div
      className={
        variant === "hero"
          ? "install-block install-block--hero"
          : "install-block"
      }
    >
      {(headingLabel || allowSkillSelect) && (
        <div className="install-head">
          {allowSkillSelect ? (
            <label className="install-label" htmlFor={selectId}>
              {headingLabel}
            </label>
          ) : (
            <span className="install-label">{headingLabel}</span>
          )}
          <span role="status" className="install-status" data-state={status}>
            {statusMessage}
          </span>
        </div>
      )}

      {!headingLabel && !allowSkillSelect && (
        <div className="install-head install-head--status-only">
          <span role="status" className="install-status" data-state={status}>
            {statusMessage}
          </span>
        </div>
      )}

      {allowSkillSelect && (
        <select
          id={selectId}
          className="field install-select"
          value={selectedSkill}
          onChange={(event) => handleSkillChange(event.target.value)}
        >
          <option value="all">Tất cả 4 skill (mặc định)</option>
          {starterSkills.map((skill) => (
            <option key={skill.id} value={skill.id}>
              {skill.id} — {skill.title}
            </option>
          ))}
        </select>
      )}

      <div className="install-command">
        <span className="install-prompt" aria-hidden="true">
          $
        </span>
        <code id={codeId} ref={codeRef}>
          {command}
        </code>
        <button
          ref={buttonRef}
          type="button"
          className="install-copy"
          data-copied={status === "copied" ? "" : undefined}
          data-failed={status === "failed" ? "" : undefined}
          {...invokerProps}
        >
          <Icon
            name={status === "copied" ? "check" : "copy"}
            width="16"
            height="16"
          />
          <span>Sao chép</span>
          <span className="sr-only"> {accessibleTarget}</span>
        </button>
      </div>
    </div>
  );
}
