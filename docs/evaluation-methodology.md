# Phương pháp đánh giá

## Đơn vị đánh giá

Mỗi case gồm input, context, skill, domain, register, constraints, pattern dự kiến, nội dung phải giữ, nội dung cấm thêm và blocker cụ thể. Reviewer không phải viết đúng một đáp án mẫu.

## Quy trình reviewer

1. Đọc input và context, rồi lập danh sách bảo toàn trước khi nhìn output.
2. Kiểm blocker: dữ kiện, số, tên, ngày, mức chắc chắn, lập trường, nguồn, điều kiện, ngoại lệ, thuật ngữ, trải nghiệm, nguyên nhân và metric.
3. Nếu không có blocker, chấm tám tiêu chí từ 1 đến 5.
4. Ghi lý do cho điểm 1 hoặc 2 và mọi bất đồng về register.
5. Với case không nên sửa, tập trung vào edit necessity và over-editing avoidance.

Output có blocker bị xem là fail dù câu trôi chảy hoặc điểm trung bình cao. Reviewer phải chọn blocker từ enum trong `benchmarks/review-result.schema.json`.

## Nhiều reviewer

Mỗi dòng kết quả có `case_id`, `system` và `reviewer_id`, vì vậy một case có thể nhận nhiều review độc lập. Runner tính trung bình trên các review hợp lệ, số reviewer, blocker rate, số case đã review và số case chưa review.

Runner cố ý không tính inter-rater agreement. Agreement cần đủ overlap giữa reviewer, lựa chọn statistic phù hợp thang ordinal và kế hoạch xử lý dữ liệu thiếu. Khi có dữ liệu thật, báo cả điểm gốc và bất đồng thay vì chỉ giữ một số trung bình.

## Báo cáo

Báo điểm theo skill, domain, register và pattern khi cỡ mẫu cho phép. Luôn tách blocker rate khỏi average. Không quy đổi điểm thành xác suất văn bản do AI tạo.

Repository chưa có human-reviewed baseline. Benchmark hiện chỉ hỗ trợ regression dữ liệu và chuẩn hóa quy trình review, không chứng minh hiệu quả ngoài 30 case.
