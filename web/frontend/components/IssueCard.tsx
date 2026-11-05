import React, { useId, useState } from "react";
import type { IssueItem, IssueOccurrence, PatternItem } from "../lib/types";
import styles from "./workspace.module.css";

interface IssueCardProps {
  issue: IssueItem;
  pattern?: PatternItem;
  onSelectPattern?: (patternId: string) => void;
}
const SEVERITY_LABELS: Record<string, string> = {
  high: "Cao",
  medium: "Vừa",
  low: "Thấp",
  error: "Lỗi",
  warning: "Cảnh báo",
  heuristic: "Tham khảo",
  preference: "Tùy chọn",
};
const FINDING_LABELS: Record<string, string> = {
  error: "Lỗi cần sửa",
  warning: "Cần xem lại",
  preference: "Lựa chọn cách viết",
  heuristic: "Tín hiệu tham khảo",
};

export const IssueCard: React.FC<IssueCardProps> = ({
  issue,
  pattern,
  onSelectPattern,
}) => {
  const [showOccurrences, setShowOccurrences] = useState(false);
  const occurrenceId = useId();
  const occurrences: IssueOccurrence[] = issue.occurrences?.length
    ? issue.occurrences
    : [
        {
          line: issue.line,
          column: issue.column,
          excerpt: issue.excerpt,
          matched_text: "",
        },
      ];
  const severity = issue.severity.toLowerCase();
  const severityColor = ["high", "error"].includes(severity)
    ? styles.danger
    : ["medium", "warning"].includes(severity)
      ? styles.warning
      : undefined;
  const renderExcerpt = (occurrence: IssueOccurrence) => {
    const index = occurrence.matched_text
      ? occurrence.excerpt.indexOf(occurrence.matched_text)
      : -1;
    if (index < 0) return occurrence.excerpt;
    const end = index + occurrence.matched_text.length;
    return (
      <>
        {occurrence.excerpt.slice(0, index)}
        <mark>{occurrence.excerpt.slice(index, end)}</mark>
        {occurrence.excerpt.slice(end)}
      </>
    );
  };
  return (
    <article className={styles.finding}>
      <div className={styles.findingType}>
        <span className={severityColor}>
          {FINDING_LABELS[issue.finding_type] ?? issue.finding_type}
        </span>
        <span>Mức độ: {SEVERITY_LABELS[severity] ?? issue.severity}</span>
      </div>
      <h3 className={styles.findingTitle}>{issue.message}</h3>
      <div className={styles.findingMeta}>
        <span className={styles.identifier}>{issue.pattern_id}</span>
        <span>
          Dòng {issue.line}, cột {issue.column}
        </span>
        {occurrences.length > 1 && (
          <button
            type="button"
            aria-expanded={showOccurrences}
            aria-controls={occurrenceId}
            onClick={() => setShowOccurrences((current) => !current)}
            className="text-link"
          >
            {occurrences.length} vị trí
          </button>
        )}
      </div>
      <blockquote className={styles.excerpt}>
        “{renderExcerpt(occurrences[0])}”
      </blockquote>
      {showOccurrences && occurrences.length > 1 && (
        <ol
          id={occurrenceId}
          className={styles.occurrences}
          aria-label="Các vị trí phát hiện"
        >
          {occurrences.map((occurrence, index) => (
            <li key={`${occurrence.line}-${occurrence.column}-${index}`}>
              <p>
                Dòng {occurrence.line}, cột {occurrence.column}
              </p>
              <p>“{renderExcerpt(occurrence)}”</p>
            </li>
          ))}
        </ol>
      )}
      {issue.suggestion && (
        <p className={styles.suggestion}>
          <strong>Gợi ý sửa: </strong>
          {issue.suggestion}
        </p>
      )}
      {pattern && (
        <details
          className={styles.explanation}
          onToggle={(event) => {
            if (event.currentTarget.open) onSelectPattern?.(issue.pattern_id);
          }}
        >
          <summary>Vì sao có gợi ý này?</summary>
          <div className={styles.explanationBody}>
            <div>
              <h4>{pattern.name}</h4>
              <p className={styles.identifier}>{pattern.skill}</p>
            </div>
            <p>{pattern.summary}</p>
            <div>
              <h4>Vì sao cần xem lại?</h4>
              <p>{pattern.why_it_matters}</p>
            </div>
            {pattern.rewrite_strategy && (
              <div>
                <h4>Gợi ý diễn đạt lại</h4>
                <p>{pattern.rewrite_strategy}</p>
              </div>
            )}
          </div>
        </details>
      )}
    </article>
  );
};
