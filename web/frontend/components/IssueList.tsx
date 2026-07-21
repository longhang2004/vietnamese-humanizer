import React, { useState } from "react";
import { IssueItem, LintSummary, PatternItem } from "../lib/types";
import { IssueCard } from "./IssueCard";

interface IssueListProps {
  summary: LintSummary;
  issues: IssueItem[];
  patterns: PatternItem[];
}

export const IssueList: React.FC<IssueListProps> = ({ summary, issues, patterns }) => {
  const [selectedPattern, setSelectedPattern] = useState<PatternItem | null>(null);
  const [filterType, setFilterType] = useState<string>("all");

  const patternMap = new Map<string, PatternItem>();
  patterns.forEach((p) => patternMap.set(p.id, p));

  const handleSelectPattern = (patternId: string) => {
    const pat = patternMap.get(patternId);
    if (pat) {
      setSelectedPattern(pat);
    }
  };

  const filteredIssues = issues.filter((issue) => {
    if (filterType === "all") return true;
    return issue.finding_type === filterType;
  });

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 mb-6">
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 mb-4 border-b border-gray-200">
        <div>
          <h2 className="text-lg font-bold text-gray-800">Kết quả rà soát</h2>
          <p className="text-xs text-gray-500 mt-0.5">{summary.note}</p>
        </div>

        <div className="flex items-center space-x-2 text-xs">
          <span className="font-semibold px-2.5 py-1 bg-gray-100 rounded-full text-gray-700">
            Tổng: {summary.total}
          </span>
          {summary.error > 0 && (
            <span className="font-semibold px-2.5 py-1 bg-red-100 text-red-800 rounded-full">
              Lỗi: {summary.error}
            </span>
          )}
          {summary.warning > 0 && (
            <span className="font-semibold px-2.5 py-1 bg-amber-100 text-amber-800 rounded-full">
              Cảnh báo: {summary.warning}
            </span>
          )}
          {summary.heuristic > 0 && (
            <span className="font-semibold px-2.5 py-1 bg-blue-100 text-blue-800 rounded-full">
              Tín hiệu: {summary.heuristic}
            </span>
          )}
        </div>
      </div>

      {issues.length === 0 ? (
        <div className="text-center py-8 bg-emerald-50 rounded-lg border border-emerald-200 text-emerald-800">
          <span className="text-2xl block mb-1">🎉</span>
          <p className="font-semibold text-sm">Không phát hiện tín hiệu bất thường!</p>
          <p className="text-xs text-emerald-700 mt-1">
            Văn bản mượt mà, tự nhiên và tuân thủ tốt các kỹ năng rà soát đã chọn.
          </p>
        </div>
      ) : (
        <div>
          <div className="flex items-center space-x-2 mb-4 text-xs">
            <span className="text-gray-500 font-medium">Lọc phát hiện:</span>
            <button
              type="button"
              onClick={() => setFilterType("all")}
              className={`px-2.5 py-1 rounded-md border ${
                filterType === "all"
                  ? "bg-brand-600 text-white border-brand-600 font-medium"
                  : "bg-gray-50 text-gray-700 border-gray-200 hover:bg-gray-100"
              }`}
            >
              Tất cả ({issues.length})
            </button>
            {summary.heuristic > 0 && (
              <button
                type="button"
                onClick={() => setFilterType("heuristic")}
                className={`px-2.5 py-1 rounded-md border ${
                  filterType === "heuristic"
                    ? "bg-blue-600 text-white border-blue-600 font-medium"
                    : "bg-gray-50 text-gray-700 border-gray-200 hover:bg-gray-100"
                }`}
              >
                Tín hiệu khuôn mẫu ({summary.heuristic})
              </button>
            )}
            {summary.warning > 0 && (
              <button
                type="button"
                onClick={() => setFilterType("warning")}
                className={`px-2.5 py-1 rounded-md border ${
                  filterType === "warning"
                    ? "bg-amber-600 text-white border-amber-600 font-medium"
                    : "bg-gray-50 text-gray-700 border-gray-200 hover:bg-gray-100"
                }`}
              >
                Cảnh báo ({summary.warning})
              </button>
            )}
          </div>

          <div className="space-y-3">
            {filteredIssues.map((issue, idx) => (
              <IssueCard
                key={`${issue.pattern_id}-${issue.line}-${issue.column}-${idx}`}
                issue={issue}
                pattern={patternMap.get(issue.pattern_id)}
                onSelectPattern={handleSelectPattern}
              />
            ))}
          </div>
        </div>
      )}

      {/* Pattern Detail Modal */}
      {selectedPattern && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full p-6 shadow-xl relative max-h-[90vh] overflow-y-auto">
            <button
              type="button"
              onClick={() => setSelectedPattern(null)}
              className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 text-xl font-bold"
            >
              ✕
            </button>
            <div className="flex items-center space-x-2 mb-2">
              <span className="font-mono text-sm bg-brand-100 text-brand-800 px-2 py-0.5 rounded font-bold">
                {selectedPattern.id}
              </span>
              <span className="text-xs text-gray-500 uppercase tracking-wide font-semibold">
                {selectedPattern.skill}
              </span>
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">{selectedPattern.name}</h3>
            <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded mb-4 border border-gray-200">
              {selectedPattern.summary}
            </p>

            <div className="space-y-3 text-sm">
              <div>
                <h4 className="font-semibold text-gray-800 text-xs uppercase tracking-wider text-amber-900">
                  Tại sao điều này quan trọng:
                </h4>
                <p className="text-gray-700 mt-1 text-xs leading-relaxed">
                  {selectedPattern.why_it_matters}
                </p>
              </div>

              {selectedPattern.rewrite_strategy && (
                <div>
                  <h4 className="font-semibold text-xs uppercase tracking-wider text-emerald-900">
                    Chiến lược gợi ý sửa:
                  </h4>
                  <p className="text-gray-700 mt-1 text-xs leading-relaxed bg-emerald-50 p-2.5 rounded border border-emerald-200">
                    {selectedPattern.rewrite_strategy}
                  </p>
                </div>
              )}
            </div>

            <div className="mt-6 flex justify-end">
              <button
                type="button"
                onClick={() => setSelectedPattern(null)}
                className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 text-xs font-semibold rounded-md"
              >
                Đóng
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
