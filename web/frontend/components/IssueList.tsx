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
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200/80 p-5 sm:p-6 mb-8 transition-all">
      {/* Header Summary Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 mb-5 border-b border-slate-100">
        <div>
          <h2 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <svg className="w-5 h-5 text-sky-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Kết quả rà soát văn phong</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1 leading-normal">{summary.note}</p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono">
          <span className="font-bold px-3 py-1 bg-slate-100 text-slate-700 rounded-full border border-slate-200/60">
            Tổng: {summary.total}
          </span>
          {summary.error > 0 && (
            <span className="font-bold px-3 py-1 bg-rose-50 text-rose-700 rounded-full border border-rose-200/80">
              Lỗi: {summary.error}
            </span>
          )}
          {summary.warning > 0 && (
            <span className="font-bold px-3 py-1 bg-amber-50 text-amber-800 rounded-full border border-amber-200/80">
              Cảnh báo: {summary.warning}
            </span>
          )}
          {summary.heuristic > 0 && (
            <span className="font-bold px-3 py-1 bg-sky-50 text-sky-800 rounded-full border border-sky-200/80">
              Tín hiệu: {summary.heuristic}
            </span>
          )}
        </div>
      </div>

      {issues.length === 0 ? (
        <div className="text-center py-10 px-4 bg-emerald-50/60 rounded-xl border border-emerald-200/80 text-emerald-950">
          <div className="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto mb-3 shadow-inner">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
            </svg>
          </div>
          <p className="font-bold text-base text-emerald-950">Không phát hiện tín hiệu bất thường!</p>
          <p className="text-xs text-emerald-700 mt-1 max-w-md mx-auto leading-relaxed">
            Văn bản diễn đạt mượt mà, tự nhiên và tuân thủ tốt các kỹ năng rà soát đã chọn.
          </p>
        </div>
      ) : (
        <div>
          {/* Filter Pills */}
          <div className="flex items-center space-x-2 mb-4 text-xs overflow-x-auto pb-1">
            <span className="text-slate-400 font-medium font-mono flex-shrink-0">Lọc tín hiệu:</span>
            <button
              type="button"
              onClick={() => setFilterType("all")}
              className={`px-3 py-1 rounded-lg font-medium transition-all ${
                filterType === "all"
                  ? "bg-slate-900 text-white font-semibold shadow-sm"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200/70"
              }`}
            >
              Tất cả ({issues.length})
            </button>
            {summary.heuristic > 0 && (
              <button
                type="button"
                onClick={() => setFilterType("heuristic")}
                className={`px-3 py-1 rounded-lg font-medium transition-all ${
                  filterType === "heuristic"
                    ? "bg-sky-600 text-white font-semibold shadow-sm shadow-sky-600/20"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200/70"
                }`}
              >
                Khuôn mẫu ({summary.heuristic})
              </button>
            )}
            {summary.warning > 0 && (
              <button
                type="button"
                onClick={() => setFilterType("warning")}
                className={`px-3 py-1 rounded-lg font-medium transition-all ${
                  filterType === "warning"
                    ? "bg-amber-600 text-white font-semibold shadow-sm shadow-amber-600/20"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200/70"
                }`}
              >
                Cảnh báo ({summary.warning})
              </button>
            )}
          </div>

          {/* Cards List */}
          <div className="space-y-3.5">
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

      {/* Pattern Detail Modal with Backdrop Blur */}
      {selectedPattern && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 transition-all">
          <div className="bg-white rounded-2xl max-w-2xl w-full p-6 sm:p-7 shadow-2xl relative max-h-[90vh] overflow-y-auto border border-slate-200 animate-in fade-in zoom-in-95 duration-150">
            <button
              type="button"
              onClick={() => setSelectedPattern(null)}
              className="absolute top-5 right-5 w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 hover:text-slate-700 flex items-center justify-center transition-colors font-bold"
            >
              ✕
            </button>

            <div className="flex items-center space-x-2.5 mb-3">
              <span className="font-mono text-xs bg-sky-100 text-sky-800 px-2.5 py-1 rounded-md font-bold border border-sky-200/80">
                {selectedPattern.id}
              </span>
              <span className="text-[11px] text-slate-400 font-mono uppercase tracking-wider font-semibold">
                {selectedPattern.skill}
              </span>
            </div>

            <h3 className="text-xl font-extrabold text-slate-900 mb-3 tracking-tight">{selectedPattern.name}</h3>
            
            <div className="text-xs sm:text-sm text-slate-700 bg-slate-50/80 p-4 rounded-xl mb-5 border border-slate-200/80 leading-relaxed font-sans">
              {selectedPattern.summary}
            </div>

            <div className="space-y-4 text-xs sm:text-sm">
              <div className="bg-amber-50/60 p-4 rounded-xl border border-amber-200/70">
                <h4 className="font-bold text-xs uppercase tracking-wider font-mono text-amber-950 mb-1 flex items-center gap-1.5">
                  <svg className="w-4 h-4 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                  </svg>
                  <span>Lý do cần gọt giũa:</span>
                </h4>
                <p className="text-amber-900 mt-1 leading-relaxed">
                  {selectedPattern.why_it_matters}
                </p>
              </div>

              {selectedPattern.rewrite_strategy && (
                <div className="bg-emerald-50/70 p-4 rounded-xl border border-emerald-200/70">
                  <h4 className="font-bold text-xs uppercase tracking-wider font-mono text-emerald-950 mb-1 flex items-center gap-1.5">
                    <svg className="w-4 h-4 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z" />
                    </svg>
                    <span>Gợi ý diễn đạt lại:</span>
                  </h4>
                  <p className="text-emerald-950 mt-1 leading-relaxed">
                    {selectedPattern.rewrite_strategy}
                  </p>
                </div>
              )}
            </div>

            <div className="mt-6 flex justify-end">
              <button
                type="button"
                onClick={() => setSelectedPattern(null)}
                className="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold rounded-xl transition-colors"
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

