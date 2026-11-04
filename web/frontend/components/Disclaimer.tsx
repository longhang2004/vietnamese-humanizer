import React from "react";

export const Disclaimer: React.FC = () => {
  return (
    <details className="max-w-2xl text-left text-xs text-slate-500">
      <summary className="cursor-pointer font-medium">Về công cụ</summary>
      <p className="mt-3 leading-relaxed">
        Công cụ gợi ý chỗ cần xem lại theo các quy tắc biên tập tiếng Việt.
        Kết quả không xác định ai viết văn bản hay chấm xác suất AI.
        Công cụ không hỗ trợ vượt qua công cụ phát hiện AI.
      </p>
    </details>
  );
};


