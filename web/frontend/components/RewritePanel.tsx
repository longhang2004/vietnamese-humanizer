import React, { useState } from "react";
import { rewriteText } from "../lib/api";
import { RewriteResponse } from "../lib/types";

interface RewritePanelProps {
  originalText: string;
  issueIds?: string[];
}

export const RewritePanel: React.FC<RewritePanelProps> = ({ originalText, issueIds }) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<RewriteResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  const handleRewrite = async () => {
    if (!originalText.trim()) return;
    setLoading(true);
    setErrorMsg(null);
    setCopied(false);
    try {
      const res = await rewriteText(originalText, "humanizer-vi", issueIds);
      setResult(res);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg("Đã xảy ra lỗi không xác định khi gọi gợi ý viết lại.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (!result?.rewrite) return;
    navigator.clipboard.writeText(result.rewrite);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200/80 p-5 sm:p-6 mb-8 transition-all">
      <div className="flex flex-wrap justify-between items-center gap-4 mb-4 pb-4 border-b border-slate-100">
        <div>
          <h2 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <svg className="w-5 h-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
            </svg>
            <span>Gợi ý viết lại tự nhiên (Gemini Lab)</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1 leading-normal">
            Tạo bản diễn đạt tự nhiên dựa trên kết quả linter, giữ nguyên dữ kiện, thông số và tên riêng.
          </p>
        </div>

        <button
          type="button"
          onClick={handleRewrite}
          disabled={loading || !originalText.trim()}
          className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs sm:text-sm rounded-xl shadow-md shadow-emerald-600/20 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none active:scale-[0.98] transition-all flex items-center space-x-2"
        >
          {loading ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              <span>Đang viết lại...</span>
            </>
          ) : (
            <>
              <svg className="w-4 h-4 text-emerald-200" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
              </svg>
              <span>Viết lại bằng Gemini</span>
            </>
          )}
        </button>
      </div>

      {errorMsg && (
        <div className="p-3.5 bg-amber-50 border border-amber-200/80 text-amber-900 rounded-xl text-xs mb-4">
          <span className="font-bold">Lưu ý hệ thống:</span> {errorMsg}
        </div>
      )}

      {result && (
        <div className="mt-4 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 bg-slate-50 p-3 rounded-xl border border-slate-200/60">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-1 bg-amber-100 text-amber-800 text-[11px] font-mono font-bold rounded-full border border-amber-200 uppercase tracking-wider">
                {result.review_status}
              </span>
              <span className="text-xs text-slate-500 italic">{result.disclaimer}</span>
            </div>

            <button
              type="button"
              onClick={handleCopy}
              className="px-3 py-1 bg-white hover:bg-slate-100 text-slate-700 text-xs font-semibold rounded-lg border border-slate-200 shadow-sm flex items-center space-x-1.5 transition-all"
            >
              {copied ? (
                <>
                  <svg className="w-3.5 h-3.5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                  </svg>
                  <span className="text-emerald-700 font-bold">Đã sao chép!</span>
                </>
              ) : (
                <>
                  <svg className="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.757c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 011.927-.184" />
                  </svg>
                  <span>Sao chép kết quả</span>
                </>
              )}
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div className="p-4 bg-slate-50/70 rounded-xl border border-slate-200/80 text-xs sm:text-sm">
              <span className="block font-bold text-slate-500 text-xs uppercase tracking-wider font-mono mb-2">
                Văn bản gốc:
              </span>
              <p className="whitespace-pre-wrap text-slate-800 leading-relaxed font-sans">{originalText}</p>
            </div>

            <div className="p-4 bg-emerald-50/70 rounded-xl border border-emerald-200/80 text-xs sm:text-sm">
              <span className="block font-bold text-emerald-800 text-xs uppercase tracking-wider font-mono mb-2 flex items-center justify-between">
                <span>Bản viết lại đề xuất:</span>
                <span className="text-[10px] text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">Cần tác giả duyệt</span>
              </span>
              <p className="whitespace-pre-wrap text-emerald-950 font-medium leading-relaxed font-sans">
                {result.rewrite}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

