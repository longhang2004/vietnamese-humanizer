import React, { useState } from "react";
import { submitContribution } from "../lib/api";
import { ContributionResponse, SkillItem } from "../lib/types";

interface ContributeFormProps {
  skills: SkillItem[];
}

export const ContributeForm: React.FC<ContributeFormProps> = ({ skills }) => {
  const [inputText, setInputText] = useState("");
  const [context, setContext] = useState("");
  const [suggestion, setSuggestion] = useState("");
  const [skill, setSkill] = useState("humanizer-vi");
  const [note, setNote] = useState("");
  const [consent, setConsent] = useState(false);

  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<ContributionResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!consent) return;
    setLoading(true);
    setErrorMsg(null);
    setResponse(null);

    try {
      const res = await submitContribution({
        input_text: inputText,
        context: context || undefined,
        suggestion,
        skill,
        note: note || undefined,
        consent,
      });
      setResponse(res);
      // Reset form fields
      setInputText("");
      setContext("");
      setSuggestion("");
      setNote("");
      setConsent(false);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg("Đã xảy ra lỗi khi gửi đề xuất đóng góp.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 max-w-3xl mx-auto my-6">
      <h2 className="text-xl font-bold text-gray-900 mb-1">Đóng góp ví dụ / Case văn phong</h2>
      <p className="text-xs text-gray-600 mb-6">
        Các đóng góp của bạn sẽ được lưu vào cơ sở dữ liệu kiểm duyệt (staging) để maintainer rà soát trước khi đưa vào bộ corpus dữ liệu chuẩn.
      </p>

      {response && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 text-emerald-900 rounded-md text-xs mb-6">
          <p className="font-bold text-sm">✅ {response.message}</p>
          <p className="mt-1">Mã đề xuất đóng góp của bạn: <code className="bg-emerald-100 px-1 py-0.5 rounded font-mono">{response.id}</code> (Trạng thái: {response.status})</p>
        </div>
      )}

      {errorMsg && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-900 rounded-md text-xs mb-6">
          <p className="font-bold">❌ Gửi thất bại:</p>
          <p className="mt-0.5">{errorMsg}</p>
        </div>
      )}

      <div className="space-y-4">
        <div>
          <label htmlFor="skill-select" className="block text-xs font-semibold text-gray-700 mb-1">
            Chọn kỹ năng liên quan <span className="text-red-500">*</span>
          </label>
          <select
            id="skill-select"
            value={skill}
            onChange={(e) => setSkill(e.target.value)}
            className="w-full p-2.5 border border-gray-300 rounded-md text-xs focus:ring-brand-500 focus:border-brand-500"
          >
            {skills.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name} ({s.id})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="input-text" className="block text-xs font-semibold text-gray-700 mb-1">
            Văn bản gốc (Input Text) <span className="text-red-500">*</span>
          </label>
          <textarea
            id="input-text"
            rows={4}
            required
            maxLength={20000}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Nhập đoạn văn bản chứa câu/từ chưa tự nhiên..."
            className="w-full p-3 border border-gray-300 rounded-md text-xs focus:ring-brand-500 focus:border-brand-500"
          />
        </div>

        <div>
          <label htmlFor="context-text" className="block text-xs font-semibold text-gray-700 mb-1">
            Ngữ cảnh văn bản (Context - Không bắt buộc)
          </label>
          <input
            id="context-text"
            type="text"
            maxLength={5000}
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="Ví dụ: Báo chí chính luận, thông cáo báo chí, email công việc..."
            className="w-full p-2.5 border border-gray-300 rounded-md text-xs focus:ring-brand-500 focus:border-brand-500"
          />
        </div>

        <div>
          <label htmlFor="suggestion-text" className="block text-xs font-semibold text-gray-700 mb-1">
            Bản gọt giũa đề xuất (Suggestion) <span className="text-red-500">*</span>
          </label>
          <textarea
            id="suggestion-text"
            rows={4}
            required
            maxLength={20000}
            value={suggestion}
            onChange={(e) => setSuggestion(e.target.value)}
            placeholder="Nhập cách diễn đạt sửa đổi tự nhiên, chuẩn mực hơn..."
            className="w-full p-3 border border-gray-300 rounded-md text-xs focus:ring-brand-500 focus:border-brand-500"
          />
        </div>

        <div>
          <label htmlFor="note-text" className="block text-xs font-semibold text-gray-700 mb-1">
            Ghi chú thêm (Note - Không bắt buộc)
          </label>
          <input
            id="note-text"
            type="text"
            maxLength={5000}
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Lý do nên sửa, quy chuẩn tham chiếu..."
            className="w-full p-2.5 border border-gray-300 rounded-md text-xs focus:ring-brand-500 focus:border-brand-500"
          />
        </div>

        <div className="pt-2 border-t border-gray-200">
          <label className="flex items-start cursor-pointer text-xs text-gray-700 font-medium">
            <input
              type="checkbox"
              checked={consent}
              onChange={(e) => setConsent(e.target.checked)}
              className="mt-0.5 mr-2.5 rounded text-brand-600 focus:ring-brand-500"
            />
            <span>
              Tôi xác nhận văn bản này không chứa thông tin cá nhân nhạy cảm (PII) và tôi có quyền chia sẻ ví dụ này để phục vụ nghiên cứu cộng đồng. <span className="text-red-500">*</span>
            </span>
          </label>
        </div>
      </div>

      <div className="mt-6 flex justify-end">
        <button
          type="submit"
          disabled={loading || !consent || !inputText.trim() || !suggestion.trim()}
          className="px-6 py-2.5 bg-brand-600 hover:bg-brand-700 text-white font-medium text-xs rounded-md shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? "Đang gửi..." : "Gửi đóng góp case"}
        </button>
      </div>
    </form>
  );
};
