# Phương pháp đánh giá

## Đơn vị đánh giá

Mỗi case gồm input, context, skill, domain, register, constraints, pattern dự kiến, expected output mode, nội dung phải giữ, nội dung cấm thêm và blocker cụ thể. Reviewer không cần viết đúng một đáp án mẫu.

Output mode có bốn giá trị. `clean_rewrite` là replacement text; `review_comment` là lời nhắc kiểm chứng; `needs_author_decision` không tự chọn giữa nhiều cách hiểu; `no_change` giữ input đã ổn. Không ép agent rewrite mọi case.

## Quy trình reviewer

1. Đọc input và context, rồi lập danh sách bảo toàn trước khi nhìn output.
2. Kiểm output mode, rồi kiểm blocker: dữ kiện, số, tên, ngày, mức chắc chắn, lập trường, nguồn, điều kiện, ngoại lệ, thuật ngữ, trải nghiệm, nguyên nhân và metric.
3. Nếu không có blocker, chấm tám tiêu chí từ 1 đến 5.
4. Ghi lý do cho điểm 1 hoặc 2 và mọi bất đồng về register.
5. Với case không nên sửa, tập trung vào edit necessity và over-editing avoidance.

Output mode sai là blocker, kể cả khi câu trôi chảy. Output có blocker là fail dù điểm trung bình cao. Reviewer phải chọn blocker từ enum trong `benchmarks/review-result.schema.json`.

## Nhiều reviewer

Mỗi dòng kết quả có `case_id`, `system` và `reviewer_id`, nên một case có thể nhận nhiều review độc lập. Runner tính trung bình trên các review hợp lệ, số reviewer, blocker rate, số case đã review và số case chưa review.

Runner không tính inter-rater agreement. Agreement cần đủ overlap giữa reviewer, statistic phù hợp thang ordinal và kế hoạch xử lý dữ liệu thiếu. Khi có dữ liệu thật, báo cả điểm gốc và bất đồng thay vì chỉ giữ một số trung bình.

## Báo cáo

Báo điểm theo skill, domain, register và pattern khi cỡ mẫu cho phép. Luôn tách blocker rate khỏi average. Không quy đổi điểm thành xác suất văn bản do AI tạo.

Repository chưa có human-reviewed baseline. Corpus hiện chỉ có provenance `agent-reviewed`; validator kiểm cấu trúc và quan hệ metadata, nhưng không chứng minh semantic equivalence. Bộ 124 case benchmark hỗ trợ regression dữ liệu và chuẩn hóa quy trình review; chưa có điểm chất lượng độc lập.

## So sánh văn phong trên đoạn dài

Ba mươi case trong `cases/naturalness.jsonl` là 15 cặp tình huống tự viết, có bản cần giữ nguyên để kiểm sửa quá tay. Giữ cả cặp trong cùng tập development hoặc test; báo số cặp cùng số case. Trường `style` là ngữ cảnh sinh đầu ra, không phải nhãn để reviewer suy đoán đáp án. Các nhãn expected mode do agent đặt vẫn cần reviewer kiểm tra.

Để so sánh hai phiên bản prompt, tạo output cho cùng input/context/style và cố định phiên bản model cùng cấu hình sinh. Nhờ ít nhất hai reviewer đọc độc lập; giấu tên hệ thống, xáo vị trí A/B và cho phép hòa. Kiểm blocker trước, rồi chấm naturalness, preservation và register fit riêng. Một câu đúng ngữ pháp vẫn có thể không hợp quan hệ người gửi–người nhận. Không lấy độ ngắn, số issue giảm hoặc việc đổi nhiều chữ làm thước đo tự nhiên.

Lưu lựa chọn A/B/hòa và lý do trong notes của kết quả review, cùng mã batch và quy tắc xáo thứ tự. Không tự tạo điểm thay người thật. Trước khi báo agreement, cần thiết kế overlap và cách xử lý bất đồng như phần nhiều reviewer ở trên.

## Writing profiles

`cases/extended-profiles.jsonl` bổ sung 18 case cho hành chính, bài đăng mạng xã hội và marketing. Đây là chín cặp đối chiếu ngữ cảnh, khác brief ở một số cặp; không diễn giải thành phép so sánh A/B. Kiểm riêng mức nghĩa vụ và định danh văn bản, giọng cộng đồng, chứng cứ thương mại, giá và điều kiện. Chưa có human review.

Hai mươi bốn case mới gồm 12 cặp, tám case cho mỗi profile `plain`, `business`, `technical`. Profile chọn tiêu chí loại bài, còn channel/register mô tả kênh và giọng. Kiểm riêng cả lựa chọn kết hợp như technical + friendly, business + chat; không đánh đồng profile với mức trang trọng.

Runner báo số case theo profile và tách kết quả theo profile/system. Chưa review được biểu diễn bằng nhóm system rỗng, không phải điểm 0. Đọc [quy trình review profile](../benchmarks/profile-review.md) để tạo baseline, giấu tên hệ thống, giữ cặp trong cùng tập và lưu bất đồng về nhãn.
