import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test, vi } from "vitest";
import { IssueCard } from "./IssueCard";
import type { IssueItem, PatternItem } from "../lib/types";

const issue: IssueItem = {
  pattern_id: "VI-HUM-L02", finding_type: "heuristic", severity: "low", confidence: "medium", scope: "document",
  line: 1, column: 1, excerpt: "Trong bối cảnh mới", message: "Cụm dẫn nhập bị lặp.", suggestion: "Viết thẳng vào ý chính.",
  occurrences: [
    { line: 1, column: 1, excerpt: "Trong bối cảnh mới", matched_text: "Trong bối cảnh" },
    { line: 3, column: 5, excerpt: "Trong bối cảnh khác", matched_text: "Trong bối cảnh" },
  ],
};
const pattern: PatternItem = {
  id: "VI-HUM-L02", name: "Cụm dẫn nhập", skill: "humanizer-vi", category: "style", finding_type: "heuristic", severity: "low",
  summary: "Dấu hiệu diễn đạt theo khuôn.", why_it_matters: "Lặp ý khiến câu dài hơn.", rewrite_strategy: "Bắt đầu từ chủ thể và hành động.",
};

test("pattern explanations open inline and preserve every explanation field", async () => {
  const user = userEvent.setup();
  render(<IssueCard issue={issue} pattern={pattern} onSelectPattern={vi.fn()} />);
  const disclosure = screen.getByText("Vì sao có gợi ý này?").closest("details");
  expect(disclosure).not.toBeNull();
  await user.click(screen.getByText("Vì sao có gợi ý này?"));
  expect(disclosure).toHaveAttribute("open");
  expect(screen.getByText("Cụm dẫn nhập")).toBeVisible();
  expect(screen.getByText("Dấu hiệu diễn đạt theo khuôn.")).toBeVisible();
  expect(screen.getByText("Lặp ý khiến câu dài hơn.")).toBeVisible();
  expect(screen.getByText("Bắt đầu từ chủ thể và hành động.")).toBeVisible();
  expect(screen.getByText("humanizer-vi")).toBeVisible();
  expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
});

test("all occurrences remain available with line positions and highlighted matches", async () => {
  const user = userEvent.setup();
  render(<IssueCard issue={issue} onSelectPattern={vi.fn()} />);
  await user.click(screen.getByRole("button", { name: "2 vị trí" }));
  expect(screen.getByRole("list", { name: "Các vị trí phát hiện" })).toHaveTextContent("Dòng 3, cột 5");
  expect(screen.getByRole("list", { name: "Các vị trí phát hiện" }).querySelectorAll("mark")).toHaveLength(2);
});
