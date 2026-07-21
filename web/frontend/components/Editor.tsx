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
    name: "Soát lỗi ngữ pháp & chính tả tiếng Việt",
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

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 mb-6">
      <div className="flex justify-between items-center mb-3">
        <label htmlFor="editor-input" className="block text-sm font-semibold text-gray-700">
          Văn bản cần rà soát văn phong
        </label>
        <button
          type="button"
          onClick={handleLoadSample}
          className="text-xs text-brand-600 hover:text-brand-700 font-medium underline"
        >
          Chèn văn bản mẫu
        </button>
      </div>

      <textarea
        id="editor-input"
        rows={7}
        maxLength={20000}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Nhập hoặc dán đoạn văn bản tiếng Việt tại đây (tối đa 20.000 ký tự)..."
        className="w-full p-3 border border-gray-300 rounded-md shadow-inner text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
      />

      <div className="flex justify-between items-center text-xs text-gray-500 mt-1 mb-4">
        <span>Ký tự: {text.length} / 20.000</span>
        {text.length >= 20000 && <span className="text-red-500">Đã đạt giới hạn tối đa</span>}
      </div>

      <div className="mb-4">
        <span className="block text-xs font-semibold text-gray-600 uppercase tracking-wider mb-2">
          Chọn bộ kỹ năng rà soát:
        </span>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {activeSkills.map((skill) => (
            <label
              key={skill.id}
              className={`flex items-start p-2.5 rounded border text-xs cursor-pointer transition-colors ${
                selectedSkills.includes(skill.id)
                  ? "bg-brand-50 border-brand-500 text-brand-900"
                  : "bg-gray-50 border-gray-200 text-gray-600 hover:bg-gray-100"
              }`}
            >
              <input
                type="checkbox"
                checked={selectedSkills.includes(skill.id)}
                onChange={() => handleToggleSkill(skill.id)}
                className="mt-0.5 mr-2.5 rounded text-brand-600 focus:ring-brand-500"
              />
              <div>
                <span className="font-semibold block">{skill.name}</span>
                <span className="text-gray-500 leading-tight block mt-0.5">{skill.when_to_use}</span>
              </div>
            </label>
          ))}
        </div>
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={loading || !text.trim() || selectedSkills.length === 0}
          className="px-6 py-2.5 bg-brand-600 hover:bg-brand-700 text-white font-medium text-sm rounded-md shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? "Đang rà soát..." : "Kiểm tra văn phong"}
        </button>
      </div>
    </form>
  );
};
