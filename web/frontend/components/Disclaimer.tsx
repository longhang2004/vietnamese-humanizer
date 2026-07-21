import React from "react";

export const Disclaimer: React.FC = () => {
  return (
    <div className="bg-amber-50 border-l-4 border-amber-500 p-4 rounded-r shadow-sm my-4">
      <div className="flex items-start">
        <div className="flex-shrink-0 text-amber-500 font-bold text-xl mr-3">ℹ</div>
        <div>
          <h3 className="text-sm font-semibold text-amber-900">
            Tuyên bố về phạm vi và mục đích công cụ
          </h3>
          <p className="text-sm text-amber-800 mt-1 leading-relaxed">
            Đây là công cụ rà soát và nêu <strong>tín hiệu văn phong tiếng Việt</strong> giúp người viết tự review và gọt giũa bài viết. Công cụ <strong>KHÔNG</strong> phải là AI-detector, <strong>KHÔNG</strong> tính điểm xác suất do AI tạo, và <strong>KHÔNG</strong> có tính năng &quot;vượt detector&quot;. Mọi phát hiện đều là gợi ý để biên tập viên kiểm chứng.
          </p>
        </div>
      </div>
    </div>
  );
};
