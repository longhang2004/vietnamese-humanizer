import React, { useState } from "react";
import type { IssueItem, LintSummary, PatternItem } from "../lib/types";
import { IssueCard } from "./IssueCard";
import styles from "./workspace.module.css";

interface IssueListProps {
  summary: LintSummary;
  issues: IssueItem[];
  patterns: PatternItem[];
}
const FILTERS = [
  { type: "all", label: "Tất cả" },
  { type: "error", label: "Lỗi" },
  { type: "warning", label: "Cảnh báo" },
  { type: "preference", label: "Lựa chọn" },
  { type: "heuristic", label: "Tham khảo" },
];

export const IssueList: React.FC<IssueListProps> = ({
  summary,
  issues,
  patterns,
}) => {
  const [filterType, setFilterType] = useState("all");
  const patternMap = new Map(patterns.map((pattern) => [pattern.id, pattern]));
  const filteredIssues =
    filterType === "all"
      ? issues
      : issues.filter((issue) => issue.finding_type === filterType);
  return (
    <section aria-labelledby="findings-title">
      <div className={styles.toolbar}>
        <h2 id="findings-title">Kết quả soát văn phong</h2>
        <span className={styles.hint}>{issues.length} mục cần xem lại</span>
      </div>
      {issues.length > 0 && (
        <div
          role="group"
          aria-label="Lọc kết quả theo loại phát hiện"
          className={styles.filters}
        >
          {FILTERS.map(({ type, label }) => {
            const count =
              type === "all"
                ? issues.length
                : issues.filter((issue) => issue.finding_type === type).length;
            return (
              <button
                key={type}
                type="button"
                aria-pressed={filterType === type}
                onClick={() => setFilterType(type)}
                className={styles.filter}
              >
                {label} ({count})
              </button>
            );
          })}
        </div>
      )}
      {issues.length === 0 ? (
        <div className={styles.noFindings}>
          <h3>Chưa thấy chỗ cần lưu ý theo các quy tắc đã chọn.</h3>
          <p>
            Kết quả này không có nghĩa văn bản đã hết lỗi. Bạn vẫn nên đọc lại
            theo ngữ cảnh.
          </p>
        </div>
      ) : filteredIssues.length === 0 ? (
        <p className={`${styles.noFindings} ${styles.hint}`}>
          Chưa có gợi ý thuộc nhóm này. Chọn “Tất cả” để xem các mục còn lại.
        </p>
      ) : (
        <div>
          {filteredIssues.map((issue, index) => (
            <IssueCard
              key={`${issue.pattern_id}-${issue.line}-${issue.column}-${index}`}
              issue={issue}
              pattern={patternMap.get(issue.pattern_id)}
            />
          ))}
        </div>
      )}
      {summary.note && (
        <details className={styles.readingNote}>
          <summary>Cách đọc các gợi ý</summary>
          <p>{summary.note}</p>
        </details>
      )}
    </section>
  );
};
