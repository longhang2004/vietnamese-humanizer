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

Repository chưa có human-reviewed baseline. Corpus hiện chỉ có provenance `agent-reviewed`; validator kiểm cấu trúc và quan hệ metadata, nhưng không chứng minh semantic equivalence. Benchmark hỗ trợ regression dữ liệu và chuẩn hóa quy trình review. Nó không chứng minh hiệu quả ngoài 33 case.
