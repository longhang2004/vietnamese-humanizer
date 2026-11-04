# Đánh giá bản biên tập

Chấm theo rubric chung trong `benchmarks/rubric.md`: naturalness, clarity, meaning preservation, factual preservation, register fit, terminology consistency, edit necessity và over-editing avoidance.

Trình tự review:

1. Kiểm blocker trước. Có blocker thì fail dù kết quả đọc trôi chảy.
2. Đối chiếu từng ý với input và context được cung cấp.
3. Đọc riêng output để đánh giá độ tự nhiên.
4. Kiểm những chỗ không cần sửa có được giữ lại không.

Với lối viết theo khuôn, đối chiếu cả bản cần sửa và phản ví dụ cần giữ trong `benchmarks/cases/formulaic-prose.jsonl`. Xét đối lập, tóm tắt, danh sách và nhịp câu theo công việc của chúng. Việc giảm số cụm thường bị gọi là “AI tell” không tự làm bản sửa tốt hơn; đặc biệt kiểm mất phủ định, mất khoảng số và bịa chi tiết thay cho ẩn dụ.

Không dùng AI detector làm thước đo chất lượng.
