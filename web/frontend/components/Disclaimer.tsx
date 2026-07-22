import React from "react";

export const Disclaimer: React.FC = () => {
  return (
    <div className="bg-sky-50/70 border border-sky-200/80 rounded-xl p-4 shadow-sm mb-6 transition-all">
      <div className="flex items-start space-x-3">
        <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-sky-100 text-sky-700 flex items-center justify-center mt-0.5">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
          </svg>
        </div>
        <div className="flex-1 text-xs sm:text-sm">
          <h3 className="font-bold text-sky-950 flex items-center gap-2">
            <span>Phạm vi & mục đích công cụ</span>
            <span className="text-[10px] font-mono px-2 py-0.2 rounded-full bg-sky-100 text-sky-800 font-semibold border border-sky-200">
              Biên tập viên
            </span>
          </h3>
          <p className="text-slate-600 mt-1 leading-relaxed">
            Công cụ nhận diện các <strong>tín hiệu văn phong tiếng Việt</strong> giúp người viết tự kiểm tra và gọt giũa bài viết. Công cụ <strong>không</strong> đo xác suất AI, <strong>không</strong> suy đoán tác giả và <strong>không</strong> có tính năng lách kiểm duyệt. Mọi ghi nhận đều là gợi ý để tác giả tự chủ quyết định.
          </p>
        </div>
      </div>
    </div>
  );
};


