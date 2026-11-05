import React, { useState } from "react";
import { submitContribution } from "../lib/api";
import type { ContributionResponse, SkillItem } from "../lib/types";
import { starterSkills } from "../lib/onboarding";
import styles from "./workspace.module.css";

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
  const activeSkills =
    skills.length > 0
      ? skills
      : starterSkills.map((item) => ({
          id: item.id,
          name: item.title,
        }));
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (loading || !consent || !inputText.trim() || !suggestion.trim()) return;
    setLoading(true);
    setErrorMsg(null);
    setResponse(null);
    try {
      const result = await submitContribution({
        input_text: inputText,
        context: context || undefined,
        suggestion,
        skill,
        note: note || undefined,
        consent,
      });
      setResponse(result);
      setInputText("");
      setContext("");
      setSuggestion("");
      setNote("");
      setConsent(false);
    } catch (error: unknown) {
      setErrorMsg(
        error instanceof Error
          ? error.message
          : "Chưa gửi được ví dụ. Bạn hãy thử lại.",
      );
    } finally {
      setLoading(false);
    }
  };
  return (
    <form
      onSubmit={handleSubmit}
      aria-busy={loading}
      className={styles.contribution}
    >
      <fieldset disabled={loading} className={styles.contributionFields}>
        <legend className="sr-only">Ví dụ biên tập tiếng Việt</legend>
        <div className={styles.contributionSkill}>
          <label htmlFor="skill-select" className={styles.formField}>
            <span>Ví dụ này cần sửa gì?</span>
            <select
              id="skill-select"
              value={skill}
              onChange={(event) => setSkill(event.target.value)}
              className="field"
              required
            >
              {activeSkills.map((item) => (
                <option key={item.id} value={item.id}>
                  {starterSkills.find((fallback) => fallback.id === item.id)
                    ?.title ?? item.name}
                </option>
              ))}
            </select>
          </label>
        </div>
        <div className={styles.textPair}>
          <label htmlFor="input-text" className={styles.formField}>
            <span>Văn bản gốc</span>
            <textarea
              id="input-text"
              rows={10}
              required
              maxLength={20000}
              value={inputText}
              onChange={(event) => setInputText(event.target.value)}
              placeholder="Dán đoạn bạn muốn góp ý hoặc sửa lại."
              className={`field ${styles.contributionText}`}
            />
          </label>
          <label htmlFor="suggestion-text" className={styles.formField}>
            <span>Bản sửa bạn đề xuất</span>
            <textarea
              id="suggestion-text"
              rows={10}
              required
              maxLength={20000}
              value={suggestion}
              onChange={(event) => setSuggestion(event.target.value)}
              placeholder="Dán bản đã sửa, giữ nguyên dữ kiện và ý nghĩa của đoạn gốc."
              className={`field ${styles.contributionText}`}
            />
          </label>
        </div>
        <div className={styles.supplementalGrid}>
          <label htmlFor="context-text" className={styles.formField}>
            <span>Ngữ cảnh (không bắt buộc)</span>
            <textarea
              id="context-text"
              rows={3}
              maxLength={5000}
              value={context}
              onChange={(event) => setContext(event.target.value)}
              placeholder="Ví dụ: email gửi đồng nghiệp để đổi lịch họp."
              className="field"
            />
          </label>
          <label htmlFor="note-text" className={styles.formField}>
            <span>Ghi chú (không bắt buộc)</span>
            <textarea
              id="note-text"
              rows={3}
              maxLength={5000}
              value={note}
              onChange={(event) => setNote(event.target.value)}
              placeholder="Bạn sửa chỗ nào, vì sao? Có quy ước nào cần theo không?"
              className="field"
            />
          </label>
        </div>
        {response && (
          <div role="status" aria-atomic="true" className={styles.feedback}>
            <h2 className={styles.feedbackSuccess}>{response.message}</h2>
            <p>
              Mã đóng góp: <code>{response.id}</code> · Trạng thái:{" "}
              {response.status === "pending" ? "Chờ xem xét" : response.status}
            </p>
          </div>
        )}
        {errorMsg && (
          <div role="alert" className={styles.feedback}>
            <h2 className={styles.danger}>Chưa gửi được ví dụ</h2>
            <p>{errorMsg}</p>
          </div>
        )}
        <div className={styles.contributionFooter}>
          <label className={styles.consent}>
            <input
              type="checkbox"
              required
              checked={consent}
              onChange={(event) => setConsent(event.target.checked)}
            />
            <span>
              Tôi xác nhận văn bản không chứa thông tin cá nhân nhạy cảm và tôi
              có quyền chia sẻ ví dụ này cho hoạt động nghiên cứu cộng đồng.
            </span>
          </label>
          <button
            type="submit"
            disabled={
              loading || !consent || !inputText.trim() || !suggestion.trim()
            }
            className="button-primary"
          >
            {loading ? "Đang gửi…" : "Gửi ví dụ"}
          </button>
        </div>
      </fieldset>
    </form>
  );
};
