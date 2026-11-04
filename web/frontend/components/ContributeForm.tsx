import React, { useState } from "react";
import { submitContribution } from "../lib/api";
import { ContributionResponse, SkillItem } from "../lib/types";
import { starterSkills } from "../lib/onboarding";

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
        setErrorMsg("Chưa gửi được ví dụ. Bạn hãy thử lại.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-[var(--surface)] rounded-lg  border border-[var(--control-border)] p-6 max-w-3xl mx-auto my-6">
      <h2 className="text-xl font-bold text-[var(--foreground)] mb-1">Góp ví dụ biên tập tiếng Việt</h2>
      <p className="text-sm text-[var(--muted)] mb-6">
        Gửi đoạn gốc và cách sửa bạn đề xuất. Nhóm duy trì sẽ xem xét trước khi thêm ví dụ vào bộ dữ liệu của dự án.
      </p>

      {response && (
        <div className="p-4 bg-[var(--surface-raised)] border border-[var(--border)] text-[var(--accent)] rounded-md text-sm mb-6">
          <p className="font-bold text-sm">✅ {response.message}</p>
          <p className="mt-1">Mã đóng góp: <code className="bg-[var(--surface-raised)] px-1 py-0.5 rounded font-mono">{response.id}</code> · Trạng thái: {response.status === "pending" ? "Chờ xem xét" : response.status}</p>
        </div>
      )}

      {errorMsg && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-900 rounded-md text-sm mb-6">
          <p className="font-bold">Chưa gửi được ví dụ</p>
          <p className="mt-0.5">{errorMsg}</p>
        </div>
      )}

      <div className="space-y-4">
        <div>
          <label htmlFor="skill-select" className="block text-sm font-semibold text-[var(--muted)] mb-1">
            Ví dụ này cần sửa gì? <span className="text-red-500">*</span>
          </label>
          <select
            id="skill-select"
            value={skill}
            onChange={(e) => setSkill(e.target.value)}
            className="field"
          >
            {skills.map((s) => (
              <option key={s.id} value={s.id}>
                {starterSkills.find((item) => item.id === s.id)?.title ?? s.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="input-text" className="block text-sm font-semibold text-[var(--muted)] mb-1">
            Văn bản gốc <span className="text-red-500">*</span>
          </label>
          <textarea
            id="input-text"
            rows={4}
            required
            maxLength={20000}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Dán đoạn bạn muốn góp ý hoặc sửa lại."
            className="field"
          />
        </div>

        <div>
          <label htmlFor="context-text" className="block text-sm font-semibold text-[var(--muted)] mb-1">
            Ngữ cảnh (không bắt buộc)
          </label>
          <input
            id="context-text"
            type="text"
            maxLength={5000}
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="Ví dụ: email gửi đồng nghiệp để đổi lịch họp."
            className="field"
          />
        </div>

        <div>
          <label htmlFor="suggestion-text" className="block text-sm font-semibold text-[var(--muted)] mb-1">
            Bản sửa bạn đề xuất <span className="text-red-500">*</span>
          </label>
          <textarea
            id="suggestion-text"
            rows={4}
            required
            maxLength={20000}
            value={suggestion}
            onChange={(e) => setSuggestion(e.target.value)}
            placeholder="Dán bản đã sửa, giữ nguyên dữ kiện và ý nghĩa của đoạn gốc."
            className="field"
          />
        </div>

        <div>
          <label htmlFor="note-text" className="block text-sm font-semibold text-[var(--muted)] mb-1">
            Ghi chú (không bắt buộc)
          </label>
          <input
            id="note-text"
            type="text"
            maxLength={5000}
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Bạn sửa chỗ nào, vì sao? Có quy ước nào cần theo không?"
            className="field"
          />
        </div>

        <div className="pt-2 border-t border-[var(--control-border)]">
          <label className="flex items-start cursor-pointer text-sm text-[var(--muted)] font-medium">
            <input
              type="checkbox"
              checked={consent}
              onChange={(e) => setConsent(e.target.checked)}
              className="mt-0.5 mr-2.5 rounded text-[var(--accent)] focus:ring-[var(--accent)]"
            />
            <span>
              Tôi xác nhận văn bản không chứa thông tin cá nhân nhạy cảm và tôi có quyền chia sẻ ví dụ này cho hoạt động nghiên cứu cộng đồng. <span className="text-red-500">*</span>
            </span>
          </label>
        </div>
      </div>

      <div className="mt-6 flex justify-end">
        <button
          type="submit"
          disabled={loading || !consent || !inputText.trim() || !suggestion.trim()}
          className="px-6 py-2.5 bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-[var(--accent-ink)] font-medium text-sm rounded-md  disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? "Đang gửi..." : "Gửi ví dụ"}
        </button>
      </div>
    </form>
  );
};
