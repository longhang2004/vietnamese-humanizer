import React, { useState } from "react";
import type { SkillItem } from "../lib/types";
import { starterSkills } from "../lib/onboarding";

interface EditorProps {
  skills: SkillItem[];
  onLint: (text: string, selectedSkills: string[]) => void;
  loading: boolean;
  onTextChange?: (text: string) => void;
  onSkillsChange?: () => void;
}

const DEFAULT_SKILLS: SkillItem[] = starterSkills.map((skill) => ({
  id: skill.id, name: skill.title, when_to_use: skill.summary, when_not_to_use: "",
}));

const SAMPLE_TEXT = `Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới. Trong bối cảnh không ngừng phát triển, thị trường yêu cầu linh hoạt. Việc thực hiện công tác kiểm tra được tổ chức bởi ban chỉ đạo nhằm nâng cao năng lực cạnh tranh.`;

export const Editor: React.FC<EditorProps> = ({ skills, onLint, loading, onTextChange, onSkillsChange }) => {
  const [text, setText] = useState("");
  const [selectedSkills, setSelectedSkills] = useState([
    "humanizer-vi", "translationese-cleaner-vi", "grammar-checker-vi", "style-guide-vi",
  ]);
  const activeSkills = DEFAULT_SKILLS.map((fallback) => skills.find((skill) => skill.id === fallback.id) ?? fallback);

  const updateText = (value: string) => {
    const nextText = value.slice(0, 20000);
    setText(nextText);
    onTextChange?.(nextText);
  };

  const handleToggleSkill = (skillId: string) => {
    setSelectedSkills((current) => current.includes(skillId)
      ? current.filter((id) => id !== skillId)
      : [...current, skillId]);
    onSkillsChange?.();
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (loading || !text.trim() || selectedSkills.length === 0) return;
    onLint(text, selectedSkills);
  };

  return (
    <form onSubmit={handleSubmit} autoComplete="off" className="surface-panel min-w-0 p-5 sm:p-6">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-x-4 gap-y-1">
        <h2 className="text-xl font-semibold tracking-tight"><label htmlFor="editor-input">Văn bản cần soát</label></h2>
        <div className="flex flex-wrap items-center gap-2">
          {text.length > 0 && <button type="button" onClick={() => updateText("")} className="text-link min-h-11 px-2 text-sm">Xóa văn bản</button>}
          <button type="button" onClick={() => updateText(SAMPLE_TEXT)} className="text-link min-h-11 px-2 text-sm">Thử văn bản mẫu</button>
        </div>
      </div>

      <textarea
        id="editor-input" rows={10} maxLength={20000} value={text}
        onChange={(event) => updateText(event.target.value)} aria-describedby="editor-help editor-count"
        placeholder="Dán hoặc nhập đoạn tiếng Việt bạn muốn soát…"
        className="field min-h-[18rem] w-full resize-y p-4 text-base leading-7"
      />
      <div id="editor-count" className="mt-3 flex flex-wrap justify-between gap-2 text-sm tabular-nums text-[var(--muted)]">
        <span>{text.length.toLocaleString("vi-VN")} / 20.000 ký tự</span>
        <span>{text.trim() ? text.trim().split(/\s+/).length.toLocaleString("vi-VN") : 0} từ</span>
        {text.length >= 20000 && <span className="w-full text-[var(--warning)]">Đã đạt giới hạn 20.000 ký tự.</span>}
      </div>
      <p id="editor-help" className="mt-3 text-sm leading-6 text-[var(--muted)]">Chọn những nhóm bạn muốn kiểm tra bên dưới.</p>

      <fieldset className="mt-7 min-w-0 border-t border-[var(--border)] pt-5">
        <legend className="float-left mb-3 flex w-full items-center justify-between gap-3 text-base font-semibold">
          <span>Bạn muốn kiểm tra gì?</span>
          <span className="text-sm font-normal tabular-nums text-[var(--muted)]">{selectedSkills.length}/{activeSkills.length} đã chọn</span>
        </legend>
        <div className="clear-both grid grid-cols-1 gap-x-5 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2">
          {activeSkills.map((skill) => {
            const copy = starterSkills.find((item) => item.id === skill.id);
            return (
              <label key={skill.id} className="flex min-h-11 cursor-pointer items-start gap-3 rounded-lg py-3 text-base">
                <input type="checkbox" name="skills" value={skill.id} checked={selectedSkills.includes(skill.id)} onChange={() => handleToggleSkill(skill.id)} className="mt-1 h-5 w-5 shrink-0 cursor-pointer accent-[var(--accent)]" />
                <span className="min-w-0">
                  <span className="block font-medium">{copy?.title ?? skill.name}</span>
                  <span className="mt-1 block text-sm leading-6 text-[var(--muted)]">{copy?.summary ?? skill.when_to_use}</span>
                </span>
              </label>
            );
          })}
        </div>
      </fieldset>

      <div className="mt-5 border-t border-[var(--border)] pt-5">
        {selectedSkills.length === 0 && <p className="mb-3 text-sm text-[var(--warning)]">Chọn ít nhất một nhóm kiểm tra để tiếp tục.</p>}
        <button type="submit" disabled={loading || !text.trim() || selectedSkills.length === 0} className="button-primary min-h-11 w-full">{loading ? "Đang kiểm tra…" : "Soát văn phong"}</button>
      </div>
    </form>
  );
};
