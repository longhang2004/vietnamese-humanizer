import { act, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, expect, test, vi } from "vitest";
import {
  buildInstallCommand,
  InstallCommand,
  resetLastAnnouncedMessageForTests,
} from "./InstallCommand";

const BASE_COMMAND = "npx skills add longhang2004/vietnamese-humanizer";
const originalClipboardDescriptor = Object.getOwnPropertyDescriptor(
  navigator,
  "clipboard",
);

function stubClipboard(writeTextImpl: () => Promise<void>) {
  const writeText = vi.fn(writeTextImpl);
  Object.defineProperty(navigator, "clipboard", {
    value: { writeText },
    configurable: true,
  });
  return writeText;
}

beforeEach(() => {
  resetLastAnnouncedMessageForTests();
});

afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
  if (originalClipboardDescriptor) {
    Object.defineProperty(navigator, "clipboard", originalClipboardDescriptor);
  } else {
    delete (navigator as { clipboard?: unknown }).clipboard;
  }
  delete (window as { CommandEvent?: unknown }).CommandEvent;
});

test("buildInstallCommand formats full pack and single skill commands", () => {
  expect(buildInstallCommand("all")).toBe(BASE_COMMAND);
  expect(buildInstallCommand("")).toBe(BASE_COMMAND);
  expect(buildInstallCommand("humanizer-vi")).toBe(
    `${BASE_COMMAND} --skill humanizer-vi`,
  );
});

test("renders bare CLI command with Invoker attributes and empty live region at rest", () => {
  render(<InstallCommand variant="hero" label="Cài trực tiếp vào AI agent" />);

  const code = screen.getByText(BASE_COMMAND);
  expect(code.tagName).toBe("CODE");
  expect(code.textContent).toBe(BASE_COMMAND);
  expect(code.id).not.toBe("");

  const button = screen.getByRole("button", {
    name: /Sao chép lệnh cài tất cả 4 skill/,
  });
  expect(button).toHaveAttribute("type", "button");
  expect(button).toHaveAttribute("command", "--copy");
  expect(button).toHaveAttribute("commandfor", code.id);
  expect(button).toBeEnabled();

  const status = screen.getByRole("status");
  expect(status).toBeEmptyDOMElement();
  expect(status).toHaveAttribute("data-state", "idle");
});

test("copies command on click, announces feedback, repeats with NBSP, and clears on timeout", async () => {
  vi.useFakeTimers();
  const writeText = stubClipboard(() => Promise.resolve());

  render(<InstallCommand />);

  const button = screen.getByRole("button", { name: /Sao chép/ });
  await act(async () => {
    fireEvent.click(button);
  });

  expect(writeText).toHaveBeenCalledTimes(1);
  expect(writeText).toHaveBeenCalledWith(BASE_COMMAND);
  expect(button).toHaveAttribute("data-copied", "");
  expect(button).toBeEnabled();

  const status = screen.getByRole("status");
  expect(status).toHaveTextContent("Đã sao chép");
  expect(status.textContent).toBe("Đã sao chép");

  await act(async () => {
    vi.advanceTimersByTime(1000);
    fireEvent.click(button);
  });

  expect(status.textContent).toBe("Đã sao chép\u00A0");

  await act(async () => {
    vi.advanceTimersByTime(1500);
  });
  expect(status.textContent).toBe("Đã sao chép\u00A0");

  await act(async () => {
    vi.advanceTimersByTime(800);
  });
  expect(button).not.toHaveAttribute("data-copied");
  expect(status).toBeEmptyDOMElement();
});

test("shows failure state when clipboard write rejects and keeps button enabled", async () => {
  stubClipboard(() => Promise.reject(new Error("denied")));

  render(<InstallCommand />);

  const button = screen.getByRole("button", { name: /Sao chép/ });
  await act(async () => {
    fireEvent.click(button);
  });

  expect(button).toHaveAttribute("data-failed", "");
  expect(button).not.toHaveAttribute("data-copied");
  expect(button).toBeEnabled();
  expect(screen.getByRole("status")).toHaveTextContent("Chưa sao chép được");
});

test("allowSkillSelect updates command to --skill <id> and clears active status", async () => {
  const writeText = stubClipboard(() => Promise.resolve());

  render(<InstallCommand allowSkillSelect />);

  const button = screen.getByRole("button", { name: /Sao chép/ });
  await act(async () => {
    fireEvent.click(button);
  });
  expect(screen.getByRole("status")).toHaveTextContent("Đã sao chép");

  const select = screen.getByLabelText("Chọn phạm vi cài");
  fireEvent.change(select, { target: { value: "humanizer-vi" } });

  expect(screen.getByRole("status")).toBeEmptyDOMElement();
  expect(
    screen.getByText(`${BASE_COMMAND} --skill humanizer-vi`),
  ).toBeInTheDocument();

  await act(async () => {
    fireEvent.click(
      screen.getByRole("button", {
        name: /Sao chép lệnh cài skill humanizer-vi/,
      }),
    );
  });
  expect(writeText).toHaveBeenLastCalledWith(
    `${BASE_COMMAND} --skill humanizer-vi`,
  );
});

test("uses Invoker command event once without double-copying on click when CommandEvent exists", async () => {
  (window as { CommandEvent?: unknown }).CommandEvent =
    function CommandEvent() {};
  const writeText = stubClipboard(() => Promise.resolve());

  render(<InstallCommand />);

  const button = screen.getByRole("button", { name: /Sao chép/ });
  const code = screen.getByText(BASE_COMMAND);

  await act(async () => {
    fireEvent.click(button);
  });
  expect(writeText).not.toHaveBeenCalled();

  const commandEvent = new Event("command") as Event & { command?: string };
  commandEvent.command = "--copy";
  await act(async () => {
    code.dispatchEvent(commandEvent);
  });

  expect(writeText).toHaveBeenCalledTimes(1);
  expect(writeText).toHaveBeenCalledWith(BASE_COMMAND);
});
