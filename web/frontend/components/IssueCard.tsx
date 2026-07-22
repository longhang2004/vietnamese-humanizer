import React from "react";
import { IssueItem, PatternItem } from "../lib/types";

interface IssueCardProps {
  issue: IssueItem;
  pattern?: PatternItem;
  onSelectPattern: (patternId: string) => void;
}

export const IssueCard: React.FC<IssueCardProps> = ({ issue, pattern, onSelectPattern }) => {
  const getSeverityBadge = (severity: string) => {
    switch (severity.toLowerCase()) {
      case "high":
      case "error":
        return "bg-rose-50 text-rose-700 border-rose-200/80";
      case "medium":
      case "warning":
        return "bg-amber-50 text-amber-800 border-amber-200/80";
      case "low":
      case "heuristic":
      case "preference":
      default:
        return "bg-sky-50 text-sky-800 border-sky-200/80";
    }
  };

  const getFindingTypeLabel = (type: string) => {
    switch (type) {
      case "error":
        return "Lỗi ngữ pháp & chính tả";
      case "warning":
        return "Cảnh báo văn phong";
      case "preference":
        return "Khuyến nghị từ ngữ";
      case "heuristic":
        return "Lối viết khuôn mẫu";
      default:
        return type;
    }
  };

  return (
    <div className="border border-slate-200/80 rounded-xl p-4 bg-white shadow-sm hover:border-sky-300 hover:shadow transition-all group">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-2.5">
        <div className="flex items-center space-x-2">
          <button
            type="button"
            onClick={() => onSelectPattern(issue.pattern_id)}
            className="font-mono text-[11px] font-bold text-sky-700 bg-sky-50 hover:bg-sky-100 px-2.5 py-1 rounded-md border border-sky-200/80 transition-colors"
          >
            {issue.pattern_id}
          </button>
          <span className="text-xs text-slate-400 font-mono">
            Line {issue.line}:{issue.column}
          </span>
          <span className="text-xs text-slate-500 font-medium">
            • {getFindingTypeLabel(issue.finding_type)}
          </span>
        </div>
        
        <span
          className={`text-[11px] px-2.5 py-0.5 rounded-full font-mono font-bold border uppercase tracking-wider ${getSeverityBadge(
            issue.severity
          )}`}
        >
          {issue.severity}
        </span>
      </div>

      {/* Excerpt Code Box */}
      <div className="my-2.5 bg-slate-50/80 p-3 rounded-lg border-l-3 border-sky-500 text-xs sm:text-sm font-mono text-slate-800 leading-relaxed overflow-x-auto">
        &quot;{issue.excerpt}&quot;
      </div>

      {/* Main Issue Explanation */}
      <p className="text-xs sm:text-sm text-slate-700 font-medium mb-2 leading-relaxed">{issue.message}</p>

      {/* Suggestion Callout */}
      {issue.suggestion && (
        <div className="mt-2.5 text-xs text-emerald-900 bg-emerald-50/80 p-2.5 rounded-lg border border-emerald-200/70 flex items-start space-x-2">
          <svg className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
          </svg>
          <div className="flex-1">
            <span className="font-bold text-emerald-950">Gợi ý sửa: </span>
            <span className="leading-relaxed">{issue.suggestion}</span>
          </div>
        </div>
      )}

      {/* Pattern details footer */}
      {pattern && (
        <div className="mt-3 pt-2.5 border-t border-slate-100 flex justify-between items-center text-xs">
          <span className="text-slate-400 truncate max-w-md italic">{pattern.summary}</span>
          <button
            type="button"
            onClick={() => onSelectPattern(issue.pattern_id)}
            className="text-sky-600 font-bold hover:text-sky-700 hover:underline flex-shrink-0 ml-2 flex items-center space-x-1"
          >
            <span>Chi tiết quy chuẩn</span>
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
            </svg>
          </button>
        </div>
      )}
    </div>
  );
};

