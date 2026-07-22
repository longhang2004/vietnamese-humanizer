import React, { useState } from "react";
import { SkillItem } from "../lib/types";

interface EditorProps {
  skills: SkillItem[];
  onLint: (text: string, selectedSkills: string[]) => void;
  loading: boolean;
}

const DEFAULT_SKILLS: SkillItem[] = [
  {
    id: "humanizer-vi",
    name: "Humanizer tiếng Việt",
    when_to_use: "Văn bản có vẻ theo khuôn, sáo, đều nhịp hoặc lệch giọng",
    when_not_to_use: "Suy đoán tác giả, lách detector, hoặc chỉ soát lỗi máy móc",
  },
  {
    id: "translationese-cleaner-vi",
    name: "Gọt dịch thuật ngữ tiếng Việt",
    when_to_use: "Văn bản dịch thô, câu bị động khiên cưỡng, lạm dụng cấu trúc dịch tiếng Anh",
    when_not_to_use: "Soát lỗi chính tả đơn thuần hoặc sửa văn bản đã tự nhiên",
  },
  {
    id: "grammar-checker-vi",
    name: "Soát lỗi ngữ pháp & chính tả",
    when_to_use: "Phát hiện lỗi sai từ ngữ, sai ngữ pháp, câu thiếu chủ/vị rõ ràng",
    when_not_to_use: "Đánh giá văn phong hay/dở hoặc quy kết văn bản do AI sinh",
  },
  {
    id: "style-guide-vi",
    name: "Quy chuẩn văn phong & báo chí",
    when_to_use: "Rà soát tính nhất quán về thuật ngữ, xưng hô, định dạng và hành văn chuyên nghiệp",
    when_not_to_use: "Sáng tạo nghệ thuật tự do hoặc thay thế quy chuẩn riêng của tòa soạn",
  },
];

const SAMPLE_TEXT = `Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới. Trong bối cảnh không ngừng phát triển, thị trường yêu cầu linh hoạt. Việc thực hiện công tác kiểm tra được tổ chức bởi ban chỉ đạo nhằm nâng cao năng lực cạnh tranh.`;

export const Editor: React.FC<EditorProps> = ({ skills, onLint, loading }) => {
  const [text, setText] = useState<string>("");
  const [selectedSkills, setSelectedSkills] = useState<string[]>([
    "humanizer-vi",
    "translationese-cleaner-vi",
    "grammar-checker-vi",
    "style-guide-vi",
  ]);

  const activeSkills = skills && skills.length > 0 ? skills : DEFAULT_SKILLS;

  const handleToggleSkill = (skillId: string) => {
    if (selectedSkills.includes(skillId)) {
      setSelectedSkills(selectedSkills.filter((id) => id !== skillId));
    } else {
      setSelectedSkills([...selectedSkills, skillId]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;
    onLint(text, selectedSkills);
  };

  const handleLoadSample = () => {
    setText(SAMPLE_TEXT);
  };

  const handleClear = () => {
    setText("");
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-sm border border-slate-200/80 p-5 sm:p-6 mb-8 transition-all">
      {/* Editor Header Bar */}
      <div className="flex flex-wrap justify-between items-center gap-2 mb-3">
        <label htmlFor="editor-input" className="block text-sm font-bold text-slate-800 tracking-tight flex items-center gap-2">
          <svg className="w-4 h-4 text-sky-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
          </svg>
          <span>Văn bản cần kiểm tra văn phong</span>
        </label>
        
        <div className="flex items-center space-x-3 text-xs">
          {text.length > 0 && (
            <button
              type="button"
              onClick={handleClear}
              className="text-slate-400 hover:text-slate-600 font-medium transition-colors"
            >
              Xóa văn bản
            </button>
          )}
          <button
            type="button"
            onClick={handleLoadSample}
            className="inline-flex items-center space-x-1 text-sky-600 hover:text-sky-700 font-semibold transition-colors bg-sky-50 px-2.5 py-1 rounded-md border border-sky-100"
          >
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
            </svg>
            <span>Thử văn bản mẫu</span>
          </button>
        </div>
      </div>

      {/* Textarea Canvas */}
      <div className="relative group">
        <textarea
          id="editor-input"
          rows={7}
          maxLength={20000}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Dán hoặc nhập văn bản tiếng Việt để phát hiện lối viết khuôn mẫu, từ sáo rỗng hoặc cấu trúc dịch thô..."
          className="w-full p-4 border border-slate-200 rounded-xl shadow-inner text-sm leading-relaxed text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 font-sans transition-all resize-y min-h-[160px]"
        />

        {/* Character & Word Count Counter Bar */}
        <div className="flex justify-between items-center text-xs text-slate-400 mt-1.5 mb-5 px-1 font-mono">
          <div className="flex items-center space-x-3">
            <span>Ký tự: <strong className="text-slate-600">{text.length.toLocaleString()}</strong> / 20.000</span>
            <span>Từ: <strong className="text-slate-600">{text.trim() ? text.trim().split(/\s+/).length.toLocaleString() : 0}</strong></span>
          </div>
          {text.length >= 20000 && <span className="text-rose-500 font-semibold">Đã đạt giới hạn tối đa</span>}
        </div>
      </div>

      {/* Skill Selector Grid */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2.5">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider font-mono">
            Bộ kỹ năng kiểm tra:
          </span>
          <span className="text-xs text-slate-400 font-mono">
            {selectedSkills.length}/{activeSkills.length} đã chọn
          </span>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {activeSkills.map((skill) => {
            const isSelected = selectedSkills.includes(skill.id);
            return (
              <div
                key={skill.id}
                onClick={() => handleToggleSkill(skill.id)}
                className={`p-3.5 rounded-xl border text-xs cursor-pointer transition-all duration-200 select-none ${
                  isSelected
                    ? "bg-sky-50/70 border-sky-300/80 text-sky-950 shadow-sm"
                    : "bg-slate-50/50 border-slate-200/70 text-slate-600 hover:bg-slate-100/60 hover:border-slate-300"
                }`}
              >
                <div className="flex items-start space-x-3">
                  <div
                    className={`mt-0.5 w-4 h-4 rounded border flex items-center justify-center transition-all ${
                      isSelected
                        ? "bg-sky-600 border-sky-600 text-white"
                        : "border-slate-300 bg-white"
                    }`}
                  >
                    {isSelected && (
                      <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                      </svg>
                    )}
                  </div>
                  <div className="flex-1">
                    <span className="font-bold block text-slate-900 text-xs sm:text-sm">{skill.name}</span>
                    <span className="text-slate-500 leading-normal block mt-1">{skill.when_to_use}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Action Footer */}
      <div className="flex items-center justify-between pt-2 border-t border-slate-100">
        <span className="text-xs text-slate-400 hidden sm:inline-block">
          ⚡ Tự động rà soát theo bộ quy chuẩn Agent Skills
        </span>

        <button
          type="submit"
          disabled={loading || !text.trim() || selectedSkills.length === 0}
          className="w-full sm:w-auto px-7 py-3 bg-sky-600 hover:bg-sky-700 text-white font-bold text-sm rounded-xl shadow-md shadow-sky-600/20 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none active:scale-[0.98] transition-all flex items-center justify-center space-x-2"
        >
          {loading ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              <span>Đang kiểm tra...</span>
            </>
          ) : (
            <>
              <span>Soát văn phong</span>
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </>
          )}
        </button>
      </div>
    </form>
  );
};

