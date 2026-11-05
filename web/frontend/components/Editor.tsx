import React, { useState } from "react";
import type { SkillItem } from "../lib/types";
import { starterSkills } from "../lib/onboarding";
import styles from "./workspace.module.css";

interface EditorProps {
  skills: SkillItem[];
  onLint: (text: string, selectedSkills: string[]) => void;
  loading: boolean;
  onTextChange?: (text: string) => void;
  onSkillsChange?: () => void;
}

const DEFAULT_SKILLS: SkillItem[] = starterSkills.map((skill) => ({
  id: skill.id,
  name: skill.title,
  when_to_use: skill.summary,
  when_not_to_use: "",
}));
const SAMPLE_TEXT = `Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới. Trong bối cảnh không ngừng phát triển, thị trường yêu cầu linh hoạt. Việc thực hiện công tác kiểm tra được tổ chức bởi ban chỉ đạo nhằm nâng cao năng lực cạnh tranh.`;

export const Editor: React.FC<EditorProps> = ({
  skills,
  onLint,
  loading,
  onTextChange,
  onSkillsChange,
}) => {
  const [text, setText] = useState("");
  const [selectedSkills, setSelectedSkills] = useState([
    "humanizer-vi",
    "translationese-cleaner-vi",
    "grammar-checker-vi",
    "style-guide-vi",
  ]);
  const activeSkills = DEFAULT_SKILLS.map(
    (fallback) => skills.find((skill) => skill.id === fallback.id) ?? fallback,
  );
  const updateText = (value: string) => {
    const nextText = value.slice(0, 20000);
    setText(nextText);
    onTextChange?.(nextText);
  };
  const handleToggleSkill = (skillId: string) => {
    setSelectedSkills((current) =>
      current.includes(skillId)
        ? current.filter((id) => id !== skillId)
        : [...current, skillId],
    );
    onSkillsChange?.();
  };
  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (loading || !text.trim() || selectedSkills.length === 0) return;
    onLint(text, selectedSkills);
  };

  return (
    <form onSubmit={handleSubmit} autoComplete="off" className={styles.source}>
      <div className={styles.toolbar}>
        <h2>
          <label htmlFor="editor-input">Văn bản cần soát</label>
        </h2>
        <div className={styles.textActions}>
          {text.length > 0 && (
            <button
              type="button"
              onClick={() => updateText("")}
              className="text-link"
            >
              Xóa văn bản
            </button>
          )}
          <button
            type="button"
            onClick={() => updateText(SAMPLE_TEXT)}
            className="text-link"
          >
            Thử văn bản mẫu
          </button>
        </div>
      </div>
      <textarea
        id="editor-input"
        rows={12}
        maxLength={20000}
        value={text}
        onChange={(event) => updateText(event.target.value)}
        aria-describedby="editor-count"
        placeholder="Dán hoặc nhập đoạn tiếng Việt bạn muốn soát…"
        className={`field ${styles.editor}`}
      />
      <div id="editor-count" className={styles.meta}>
        <span>{text.length.toLocaleString("vi-VN")} / 20.000 ký tự</span>
        <span>
          {text.trim()
            ? text.trim().split(/\s+/).length.toLocaleString("vi-VN")
            : 0}{" "}
          từ
        </span>
        {text.length >= 20000 && (
          <span className={styles.limit}>Đã đạt giới hạn 20.000 ký tự.</span>
        )}
      </div>
      <details className={styles.options}>
        <summary>
          <span>Nhóm kiểm tra</span>
          <span className={styles.optionCount}>
            {selectedSkills.length}/{activeSkills.length} đang bật
          </span>
        </summary>
        <fieldset>
          <legend className="sr-only">Bạn muốn kiểm tra gì?</legend>
          <div className={styles.optionGrid}>
            {activeSkills.map((skill) => {
              const copy = starterSkills.find((item) => item.id === skill.id);
              return (
                <label key={skill.id} className={styles.checkOption}>
                  <input
                    type="checkbox"
                    name="skills"
                    value={skill.id}
                    checked={selectedSkills.includes(skill.id)}
                    onChange={() => handleToggleSkill(skill.id)}
                  />
                  <span>
                    <strong>{copy?.title ?? skill.name}</strong>
                    <small>{copy?.summary ?? skill.when_to_use}</small>
                  </span>
                </label>
              );
            })}
          </div>
        </fieldset>
      </details>
      <div className={styles.submitRow}>
        {selectedSkills.length === 0 && (
          <p className={styles.warning}>
            Chọn ít nhất một nhóm kiểm tra để tiếp tục.
          </p>
        )}
        <button
          type="submit"
          disabled={loading || !text.trim() || selectedSkills.length === 0}
          className={`button-primary ${styles.editorSubmit}`}
        >
          {loading ? "Đang kiểm tra…" : "Soát văn phong"}
        </button>
      </div>
    </form>
  );
};
