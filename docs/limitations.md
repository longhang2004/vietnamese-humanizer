# Giới hạn

- 40 pattern do maintainer tổng hợp, chưa được hiệu chỉnh trên corpus đại diện.
- 100 example đã được audit về preservation nhưng chưa đại diện đầy đủ cho vùng miền, thế hệ, ngành nghề hoặc register tiếng Việt.
- Nhận định “tự nhiên” phụ thuộc độc giả và mục đích. Một cách nói hợp với blog miền Nam có thể không hợp thông báo hành chính, nhưng điều đó không khiến nó sai.
- Pattern có false positive, đặc biệt với nhịp câu, bị động, từ viết tắt, đại từ và định dạng theo style riêng.
- Regex chỉ thấy tín hiệu bề mặt. Nó bỏ sót paraphrase và không phát hiện được mọi thay đổi về nghĩa, nguyên nhân, phạm vi hoặc mức chắc chắn.
- Validator kiểm cấu trúc, tham chiếu và trạng thái review. Nó không thể chứng minh semantic preservation tự động.
- Cách tách câu dựa trên dấu câu đơn giản, chưa xử lý hết viết tắt, danh sách và tài liệu hỗn hợp.
- CLI bảo vệ fenced code, inline code, URL và một số identifier, nhưng chưa parse mọi ngôn ngữ markup.
- Benchmark có 30 case và chưa có baseline do nhiều reviewer bản ngữ độc lập chấm. Chỉ sau review thật, điểm mới có giá trị cho so sánh trong phạm vi case đã lấy mẫu.
- Dự án tập trung văn viết. Văn nói, phụ đề, thơ và nội dung sáng tạo cần tiêu chí khác.

Không dùng số phát hiện của linter để kỷ luật người viết, xác minh gian lận hoặc xác định tác giả là người hay AI. Không dùng benchmark nhỏ này để khẳng định chất lượng chung cho mọi loại tiếng Việt.
