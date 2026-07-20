# Giới hạn của MVP

- 40 pattern do maintainer tổng hợp, chưa được hiệu chỉnh trên corpus đại diện.
- 100 ví dụ là dữ liệu biên tập tự viết, không phản ánh đầy đủ mọi vùng, thế hệ hay nghề nghiệp.
- Benchmark có 30 case và chưa có điểm từ nhiều reviewer độc lập.
- Regex chỉ nhìn tín hiệu bề mặt. Nó bỏ sót paraphrase và có thể báo nhầm thuật ngữ ngành, slogan, trích dẫn hoặc cấu trúc có chủ đích.
- Cách tách câu dựa trên dấu câu đơn giản, chưa xử lý hết viết tắt, danh sách và tài liệu hỗn hợp.
- Rule đại từ không hiểu vai trò discourse. "Người dùng" và "bạn" có thể cùng hợp lệ trong một tài liệu.
- CLI bảo vệ fenced code, inline code, URL và một số identifier, nhưng chưa parse mọi ngôn ngữ markup.
- Dự án tập trung văn viết; văn nói, phụ đề, thơ và nội dung sáng tạo cần tiêu chí khác.
- Không có mô hình NLP lớn trong MVP. Đây là lựa chọn để công cụ nhẹ và dễ audit, không phải tuyên bố rule đủ thay reviewer.

Tiếng Việt miền Bắc, Trung và Nam có từ vựng, tiểu từ và thói quen khác nhau. Văn nói khác văn viết. Pháp lý, hành chính, học thuật và từng ngành có convention riêng. "Tự nhiên" luôn phụ thuộc độc giả và mục đích.

Không dùng output của linter để kỷ luật người viết, xác minh gian lận hay kết luận nguồn gốc văn bản.
