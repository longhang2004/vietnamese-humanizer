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
        return "bg-red-100 text-red-800 border-red-200";
      case "medium":
      case "warning":
        return "bg-amber-100 text-amber-800 border-amber-200";
      case "low":
      case "heuristic":
      case "preference":
      default:
        return "bg-blue-100 text-blue-800 border-blue-200";
    }
  };

  const getFindingTypeLabel = (type: string) => {
    switch (type) {
      case "error":
        return "Lỗi ngữ pháp/chính tả";
      case "warning":
        return "Cảnh báo văn phong";
      case "preference":
        return "Khuyến nghị xưng hô/từ ngữ";
      case "heuristic":
        return "Tín hiệu lối viết khuôn mẫu";
      default:
        return type;
    }
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4 bg-white shadow-sm hover:border-brand-300 transition-all">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
        <div className="flex items-center space-x-2">
          <button
            type="button"
            onClick={() => onSelectPattern(issue.pattern_id)}
            className="font-mono text-xs font-bold text-brand-700 bg-brand-50 hover:bg-brand-100 px-2 py-0.5 rounded border border-brand-200"
          >
            {issue.pattern_id}
          </button>
          <span className="text-xs text-gray-500">
            [Dòng {issue.line}:{issue.column}]
          </span>
          <span className="text-xs text-gray-500 font-medium">
            • {getFindingTypeLabel(issue.finding_type)}
          </span>
        </div>
        <span
          className={`text-xs px-2 py-0.5 rounded font-semibold border ${getSeverityBadge(
            issue.severity
          )}`}
        >
          {issue.severity.toUpperCase()}
        </span>
      </div>

      <div className="my-2 bg-gray-50 p-2.5 rounded border-l-2 border-brand-500 text-sm font-mono text-gray-800">
        &quot;{issue.excerpt}&quot;
      </div>

      <p className="text-sm text-gray-700 font-medium mb-1">{issue.message}</p>

      {issue.suggestion && (
        <div className="mt-2 text-xs text-emerald-800 bg-emerald-50 p-2 rounded border border-emerald-100">
          <span className="font-semibold">💡 Gợi ý:</span> {issue.suggestion}
        </div>
      )}

      {pattern && (
        <div className="mt-3 pt-2 border-t border-gray-100 flex justify-between items-center text-xs">
          <span className="text-gray-500 truncate max-w-md">{pattern.summary}</span>
          <button
            type="button"
            onClick={() => onSelectPattern(issue.pattern_id)}
            className="text-brand-600 font-semibold hover:underline flex-shrink-0 ml-2"
          >
            Xem chi tiết pattern →
          </button>
        </div>
      )}
    </div>
  );
};
