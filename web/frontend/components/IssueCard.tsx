import React, { useId, useState } from "react";
import type { IssueItem, IssueOccurrence, PatternItem } from "../lib/types";

interface IssueCardProps { issue: IssueItem; pattern?: PatternItem; onSelectPattern?: (patternId: string) => void; }
const SEVERITY_LABELS: Record<string, string> = { high: "Cao", medium: "Vừa", low: "Thấp", error: "Lỗi", warning: "Cảnh báo", heuristic: "Tham khảo", preference: "Tùy chọn" };
const FINDING_LABELS: Record<string, string> = { error: "Lỗi cần sửa", warning: "Cần xem lại", preference: "Lựa chọn cách viết", heuristic: "Tín hiệu tham khảo" };

export const IssueCard: React.FC<IssueCardProps> = ({ issue, pattern, onSelectPattern }) => {
  const [showOccurrences, setShowOccurrences] = useState(false);
  const occurrenceId = useId();
  const occurrences: IssueOccurrence[] = issue.occurrences?.length ? issue.occurrences : [{ line: issue.line, column: issue.column, excerpt: issue.excerpt, matched_text: "" }];
  const severity = issue.severity.toLowerCase();
  const severityColor = ["high", "error"].includes(severity) ? "text-[var(--danger)]" : ["medium", "warning"].includes(severity) ? "text-[var(--warning)]" : "text-[var(--muted)]";

  const renderExcerpt = (occurrence: IssueOccurrence) => {
    const index = occurrence.matched_text ? occurrence.excerpt.indexOf(occurrence.matched_text) : -1;
    if (index < 0) return occurrence.excerpt;
    const end = index + occurrence.matched_text.length;
    return <>{occurrence.excerpt.slice(0, index)}<mark className="rounded-sm bg-[var(--warning)] px-0.5 text-[var(--accent-ink)]">{occurrence.excerpt.slice(index, end)}</mark>{occurrence.excerpt.slice(end)}</>;
  };

  return (
    <article className="min-w-0 border-t border-[var(--border)] pt-5">
      <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-2">
        <span className={`text-sm font-medium ${severityColor}`}>{FINDING_LABELS[issue.finding_type] ?? issue.finding_type}</span>
        <span className={`text-sm ${severityColor}`}>Mức độ: {SEVERITY_LABELS[severity] ?? issue.severity}</span>
      </div>
      <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm tabular-nums text-[var(--muted)]">
        <span className="font-mono">{issue.pattern_id}</span><span>Dòng {issue.line}, cột {issue.column}</span>
        {occurrences.length > 1 && <button type="button" aria-expanded={showOccurrences} aria-controls={occurrenceId} onClick={() => setShowOccurrences((current) => !current)} className="text-link min-h-11 px-1">{occurrences.length} vị trí</button>}
      </div>

      <blockquote className="my-4 break-words rounded-lg bg-[var(--background)] p-4 text-base leading-7">“{renderExcerpt(occurrences[0])}”</blockquote>
      {showOccurrences && occurrences.length > 1 && (
        <ol id={occurrenceId} className="mb-5 space-y-4" aria-label="Các vị trí phát hiện">{occurrences.map((occurrence, index) => <li key={`${occurrence.line}-${occurrence.column}-${index}`} className="break-words pl-4"><p className="text-sm tabular-nums text-[var(--muted)]">Dòng {occurrence.line}, cột {occurrence.column}</p><p className="mt-1 text-base leading-7">“{renderExcerpt(occurrence)}”</p></li>)}</ol>
      )}
      <p className="break-words text-base leading-7">{issue.message}</p>
      {issue.suggestion && <p className="mt-3 break-words text-base leading-7 text-[var(--muted)]"><span className="font-medium text-[var(--foreground)]">Gợi ý sửa: </span>{issue.suggestion}</p>}

      {pattern && (
        <details className="mt-3" onToggle={(event) => { if (event.currentTarget.open) onSelectPattern?.(issue.pattern_id); }}>
          <summary className="text-link min-h-11 cursor-pointer py-3 text-base">Vì sao có gợi ý này?</summary>
          <div className="space-y-4 pb-2 pt-3 text-base leading-7">
            <div><h3 className="font-semibold">{pattern.name}</h3><p className="mt-1 font-mono text-sm text-[var(--muted)]">{pattern.skill}</p></div>
            <p className="break-words text-[var(--muted)]">{pattern.summary}</p>
            <div><h4 className="font-medium">Vì sao cần xem lại?</h4><p className="mt-1 break-words text-[var(--muted)]">{pattern.why_it_matters}</p></div>
            {pattern.rewrite_strategy && <div><h4 className="font-medium">Gợi ý diễn đạt lại</h4><p className="mt-1 break-words text-[var(--muted)]">{pattern.rewrite_strategy}</p></div>}
          </div>
        </details>
      )}
    </article>
  );
};
