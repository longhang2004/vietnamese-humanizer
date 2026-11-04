import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";
import { IssueList } from "./IssueList";
import type { IssueItem } from "../lib/types";

const issues: IssueItem[] = ["error", "warning", "preference", "heuristic"].map((type) => ({
  pattern_id: `VI-${type}`, finding_type: type, severity: "low", confidence: "high", scope: "sentence",
  line: 1, column: 1, excerpt: "Một câu cần đọc lại.", message: `Finding ${type}`, suggestion: "Đọc lại theo ngữ cảnh.", occurrences: [],
}));

test("every finding type has a count and filters the visible findings", async () => {
  const user = userEvent.setup();
  render(<IssueList summary={{ total: 4, error: 1, warning: 1, preference: 1, heuristic: 1, note: "Đọc lại theo ngữ cảnh." }} issues={issues} patterns={[]} />);
  for (const [label, type] of [["Lỗi (1)", "error"], ["Cảnh báo (1)", "warning"], ["Lựa chọn (1)", "preference"], ["Tham khảo (1)", "heuristic"]]) {
    await user.click(screen.getByRole("button", { name: label }));
    expect(screen.getByText(`Finding ${type}`)).toBeInTheDocument();
    expect(screen.getAllByText(/^Finding /)).toHaveLength(1);
    expect(screen.getByRole("button", { name: label })).toHaveAttribute("aria-pressed", "true");
  }
  await user.click(screen.getByRole("button", { name: "Tất cả (4)" }));
  expect(screen.getAllByText(/^Finding /)).toHaveLength(4);
});

test("no findings still asks the author to review the context", () => {
  render(<IssueList summary={{ total: 0, error: 0, warning: 0, preference: 0, heuristic: 0, note: "" }} issues={[]} patterns={[]} />);
  expect(screen.getByText(/không có nghĩa văn bản đã hết lỗi/i)).toBeInTheDocument();
});
