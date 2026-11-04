import { act, fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, expect, test, vi } from "vitest";
import { CapabilityProvider } from "./CapabilityNav";
import { Checker } from "./Checker";
import { fetchHealth, fetchPatterns, fetchSkills, lintText } from "../lib/api";
import type { LintResponse } from "../lib/types";

vi.mock("../lib/api", () => ({
  fetchHealth: vi.fn(), fetchPatterns: vi.fn(), fetchSkills: vi.fn(),
  lintText: vi.fn(), rewriteText: vi.fn(),
}));

function response(message: string): LintResponse {
  return {
    version: "test",
    summary: { total: 1, error: 0, warning: 1, preference: 0, heuristic: 0, note: "Cần đọc lại theo ngữ cảnh." },
    issues: [{ pattern_id: "VI-GRA-L01", finding_type: "warning", severity: "medium", confidence: "high", scope: "sentence", line: 1, column: 1, excerpt: "Văn bản", message, suggestion: "Đọc lại câu này.", occurrences: [] }],
  };
}

beforeEach(() => {
  vi.resetAllMocks();
  vi.mocked(fetchSkills).mockResolvedValue({ skills: [] });
  vi.mocked(fetchPatterns).mockResolvedValue({ patterns: [] });
  vi.mocked(fetchHealth).mockResolvedValue({ status: "ok", version: "test", capabilities: { rewrite: false, contributions: false } });
});

function renderChecker() {
  render(<CapabilityProvider><Checker /></CapabilityProvider>);
}

test("a late result cannot replace the result for the current text", async () => {
  const user = userEvent.setup();
  let resolveA!: (value: LintResponse) => void;
  let resolveB!: (value: LintResponse) => void;
  vi.mocked(lintText)
    .mockImplementationOnce(() => new Promise((resolve) => { resolveA = resolve; }))
    .mockImplementationOnce(() => new Promise((resolve) => { resolveB = resolve; }));
  renderChecker();
  const input = screen.getByRole("textbox", { name: "Văn bản cần soát" });
  fireEvent.change(input, { target: { value: "Văn bản A" } });
  await user.click(screen.getByRole("button", { name: "Soát văn phong" }));
  fireEvent.change(input, { target: { value: "Văn bản B" } });
  await user.click(screen.getByRole("button", { name: "Soát văn phong" }));
  await act(async () => { resolveB(response("Kết quả của B")); });
  expect(await screen.findByText("Kết quả của B")).toBeInTheDocument();
  await act(async () => { resolveA(response("Kết quả cũ của A")); });
  expect(screen.queryByText("Kết quả cũ của A")).not.toBeInTheDocument();
  expect(screen.getByText("Kết quả của B")).toBeInTheDocument();
});

test("editing a pending check hides its response before another check is submitted", async () => {
  const user = userEvent.setup();
  let resolveCheck!: (value: LintResponse) => void;
  vi.mocked(lintText).mockImplementation(() => new Promise((resolve) => { resolveCheck = resolve; }));
  renderChecker();
  const input = screen.getByRole("textbox", { name: "Văn bản cần soát" });
  fireEvent.change(input, { target: { value: "Văn bản đang kiểm tra" } });
  await user.click(screen.getByRole("button", { name: "Soát văn phong" }));
  expect(screen.getByText("Đang kiểm tra văn bản. Vui lòng chờ kết quả.")).toHaveAttribute("aria-live", "polite");
  fireEvent.change(input, { target: { value: "Văn bản mới chưa gửi" } });
  await act(async () => { resolveCheck(response("Kết quả của văn bản trước")); });
  expect(screen.queryByText("Kết quả của văn bản trước")).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Soát văn phong" })).toBeEnabled();
});

test.each(["typing", "sample", "clear", "skills"])("%s invalidates the displayed result", async (change) => {
  const user = userEvent.setup();
  vi.mocked(lintText).mockResolvedValue(response("Kết quả đã cũ"));
  renderChecker();
  fireEvent.change(screen.getByRole("textbox", { name: "Văn bản cần soát" }), { target: { value: "Văn bản A" } });
  await user.click(screen.getByRole("button", { name: "Soát văn phong" }));
  expect(await screen.findByText("Kết quả đã cũ")).toBeInTheDocument();
  if (change === "typing") fireEvent.change(screen.getByRole("textbox"), { target: { value: "Văn bản B" } });
  if (change === "sample") await user.click(screen.getByRole("button", { name: "Thử văn bản mẫu" }));
  if (change === "clear") await user.click(screen.getByRole("button", { name: "Xóa văn bản" }));
  if (change === "skills") await user.click(screen.getAllByRole("checkbox")[0]);
  expect(screen.queryByText("Kết quả đã cũ")).not.toBeInTheDocument();
});

test("a late failed request does not clear a newer successful result", async () => {
  const user = userEvent.setup();
  let rejectA!: (reason: Error) => void;
  vi.mocked(lintText)
    .mockImplementationOnce(() => new Promise((_resolve, reject) => { rejectA = reject; }))
    .mockResolvedValueOnce(response("Kết quả hiện tại"));
  renderChecker();
  const input = screen.getByRole("textbox");
  fireEvent.change(input, { target: { value: "A" } });
  await user.click(screen.getByRole("button", { name: "Soát văn phong" }));
  fireEvent.change(input, { target: { value: "B" } });
  await user.click(screen.getByRole("button", { name: "Soát văn phong" }));
  expect(await screen.findByText("Kết quả hiện tại")).toBeInTheDocument();
  await act(async () => { rejectA(new Error("Lỗi yêu cầu cũ")); });
  expect(screen.queryByText("Lỗi yêu cầu cũ")).not.toBeInTheDocument();
  expect(screen.getByText("Kết quả hiện tại")).toBeInTheDocument();
});

test("a failed check provides an alert and can be retried", async () => {
  const user = userEvent.setup();
  vi.mocked(lintText).mockRejectedValueOnce(new Error("Máy chủ chưa phản hồi.")).mockResolvedValueOnce(response("Đã thử lại"));
  renderChecker();
  fireEvent.change(screen.getByRole("textbox"), { target: { value: "Văn bản cần soát" } });
  await user.click(screen.getByRole("button", { name: "Soát văn phong" }));
  expect(await screen.findByRole("alert")).toHaveTextContent("Máy chủ chưa phản hồi.");
  await user.click(screen.getByRole("button", { name: "Soát văn phong" }));
  expect(await screen.findByText("Đã thử lại")).toBeInTheDocument();
  expect(screen.queryByRole("alert")).not.toBeInTheDocument();
});

test("a network failure explains recovery in Vietnamese and preserves the draft", async () => {
  const user = userEvent.setup();
  vi.mocked(lintText).mockRejectedValue(new TypeError("Failed to fetch"));
  renderChecker();
  fireEvent.change(screen.getByRole("textbox"), { target: { value: "Bản nháp đang viết" } });
  await user.click(screen.getByRole("button", { name: "Soát văn phong" }));
  expect(await screen.findByRole("alert")).toHaveTextContent("Chưa kết nối được máy chủ. Bạn hãy thử lại sau.");
  expect(screen.getByRole("textbox")).toHaveValue("Bản nháp đang viết");
  expect(screen.getByRole("button", { name: "Soát văn phong" })).toBeEnabled();
});

test("rewrite remains hidden when capabilities cannot be loaded", async () => {
  const user = userEvent.setup();
  vi.mocked(fetchHealth).mockRejectedValue(new Error("offline"));
  vi.mocked(lintText).mockResolvedValue(response("Có thể soát khi không bật viết lại"));
  renderChecker();
  fireEvent.change(screen.getByRole("textbox"), { target: { value: "Văn bản" } });
  await user.click(screen.getByRole("button", { name: "Soát văn phong" }));
  expect(await screen.findByText("Có thể soát khi không bật viết lại")).toBeInTheDocument();
  expect(screen.queryByRole("button", { name: /Viết lại bằng Gemini/i })).not.toBeInTheDocument();
});

test("rewrite is available only for a current result when the capability is enabled", async () => {
  const user = userEvent.setup();
  vi.mocked(fetchHealth).mockResolvedValue({ status: "ok", version: "test", capabilities: { rewrite: true, contributions: false } });
  vi.mocked(lintText).mockResolvedValue(response("Kết quả hiện tại có thể viết lại"));
  renderChecker();
  expect(screen.queryByRole("button", { name: /Viết lại bằng Gemini/i })).not.toBeInTheDocument();
  fireEvent.change(screen.getByRole("textbox"), { target: { value: "Văn bản" } });
  await user.click(screen.getByRole("button", { name: "Soát văn phong" }));
  expect(await screen.findByRole("button", { name: /Viết lại bằng Gemini/i })).toBeInTheDocument();
  fireEvent.change(screen.getByRole("textbox", { name: "Văn bản cần soát" }), { target: { value: "Văn bản chưa soát" } });
  expect(screen.queryByRole("button", { name: /Viết lại bằng Gemini/i })).not.toBeInTheDocument();
});
