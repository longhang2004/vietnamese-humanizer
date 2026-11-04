import React, { useState } from "react";
import type { IssueItem, LintSummary, PatternItem } from "../lib/types";
import { IssueCard } from "./IssueCard";

interface IssueListProps { summary: LintSummary; issues: IssueItem[]; patterns: PatternItem[]; }

const FILTERS = [
  { type: "all", label: "Tất cả" }, { type: "error", label: "Lỗi" }, { type: "warning", label: "Cảnh báo" },
  { type: "preference", label: "Lựa chọn" }, { type: "heuristic", label: "Tham khảo" },
];

export const IssueList: React.FC<IssueListProps> = ({ summary, issues, patterns }) => {
  const [filterType, setFilterType] = useState("all");
  const patternMap = new Map(patterns.map((pattern) => [pattern.id, pattern]));
  const filteredIssues = filterType === "all" ? issues : issues.filter((issue) => issue.finding_type === filterType);

  return (
    <section className="surface-panel min-w-0 p-5 sm:p-6" aria-labelledby="findings-title">
      <h2 id="findings-title" className="text-xl font-semibold tracking-tight">Kết quả soát văn phong</h2>
      <p className="mt-3 text-base leading-7 text-[var(--muted)]">{issues.length} mục cần xem lại. Chọn một nhóm để tập trung vào phần cần sửa.</p>
      <div role="group" aria-label="Lọc kết quả theo loại phát hiện" className="my-5 flex flex-wrap gap-2">
        {FILTERS.map(({ type, label }) => {
          const count = type === "all" ? issues.length : issues.filter((issue) => issue.finding_type === type).length;
          return <button key={type} type="button" aria-pressed={filterType === type} onClick={() => setFilterType(type)} className={`min-h-11 rounded-lg border px-3 py-2 text-sm font-medium tabular-nums transition-colors ${filterType === type ? "border-[var(--accent)] bg-[var(--accent)] text-[var(--accent-ink)]" : "border-[var(--border)] bg-[var(--surface)] text-[var(--muted)] hover:bg-[var(--surface-raised)] hover:text-[var(--foreground)]"}`}>{label} ({count})</button>;
        })}
      </div>

      {issues.length === 0 ? (
        <div className="border-t border-[var(--border)] py-8"><h3 className="text-lg font-medium">Chưa thấy chỗ cần lưu ý theo các quy tắc đã chọn.</h3><p className="mt-3 text-base leading-7 text-[var(--muted)]">Kết quả này không có nghĩa văn bản đã hết lỗi. Bạn vẫn nên đọc lại theo ngữ cảnh.</p></div>
      ) : filteredIssues.length === 0 ? (
        <p className="border-t border-[var(--border)] py-8 text-base leading-7 text-[var(--muted)]">Chưa có gợi ý thuộc nhóm này. Chọn “Tất cả” để xem các mục còn lại.</p>
      ) : (
        <div className="space-y-6">{filteredIssues.map((issue, index) => <IssueCard key={`${issue.pattern_id}-${issue.line}-${issue.column}-${index}`} issue={issue} pattern={patternMap.get(issue.pattern_id)} />)}</div>
      )}
      {summary.note && <details className="mt-5 border-t border-[var(--border)] pt-3 text-sm text-[var(--muted)]"><summary className="min-h-11 cursor-pointer py-2">Cách đọc các gợi ý</summary><p className="mt-2 leading-7">{summary.note}</p></details>}
    </section>
  );
};
