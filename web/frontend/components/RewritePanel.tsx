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

  const handleRewrite = async () => {
    if (!originalText.trim()) return;
    setLoading(true);
    setErrorMsg(null);
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

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 mb-6">
      <div className="flex flex-wrap justify-between items-center gap-2 mb-4 pb-3 border-b border-gray-200">
        <div>
          <h2 className="text-lg font-bold text-gray-800">Thử nghiệm Gợi ý viết lại (Gemini Lab)</h2>
          <p className="text-xs text-gray-500">
            Sử dụng mô hình ngôn ngữ sinh bản viết lại bảo toàn dữ kiện, tên riêng và thông số.
          </p>
        </div>

        <button
          type="button"
          onClick={handleRewrite}
          disabled={loading || !originalText.trim()}
          className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-xs rounded-md shadow-sm disabled:opacity-50 transition-colors flex items-center space-x-1.5"
        >
          {loading ? (
            <span>Đang tạo gợi ý...</span>
          ) : (
            <>
              <span>✨ Gợi ý viết lại bằng Gemini</span>
            </>
          )}
        </button>
      </div>

      {errorMsg && (
        <div className="p-3 bg-amber-50 border border-amber-200 text-amber-900 rounded text-xs mb-4">
          <span className="font-semibold">Lưu ý:</span> {errorMsg}
        </div>
      )}

      {result && (
        <div className="mt-4 space-y-4">
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 bg-amber-100 text-amber-800 text-xs font-bold rounded-full uppercase tracking-wider border border-amber-200">
              Trạng thái: {result.review_status} (Cần review)
            </span>
            <span className="text-xs text-gray-500 italic">{result.disclaimer}</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-3 bg-gray-50 rounded border border-gray-200 text-xs">
              <span className="block font-semibold text-gray-600 mb-1">Văn bản gốc:</span>
              <p className="whitespace-pre-wrap text-gray-800 leading-relaxed">{originalText}</p>
            </div>

            <div className="p-3 bg-emerald-50 rounded border border-emerald-200 text-xs">
              <span className="block font-semibold text-emerald-900 mb-1">
                Gợi ý viết lại (cần kiểm chứng):
              </span>
              <p className="whitespace-pre-wrap text-emerald-950 font-medium leading-relaxed">
                {result.rewrite}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
