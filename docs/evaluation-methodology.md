# Phương pháp đánh giá

## Đơn vị đánh giá

Mỗi case gồm input, skill, domain, register, ràng buộc, pattern dự kiến, nội dung phải giữ và nội dung cấm thêm. Reviewer không phải viết đúng một đáp án mẫu.

## Quy trình reviewer

1. Đọc input và lập danh sách bảo toàn trước khi nhìn output.
2. Kiểm tám blocker trong `benchmarks/rubric.md`.
3. Nếu không có blocker, chấm tám tiêu chí từ 1 đến 5.
4. Ghi lý do cho điểm 1 hoặc 2 và mọi bất đồng về register.
5. Với case "không sửa", đánh giá edit necessity và over-editing avoidance như tiêu chí chính.

## Thiết kế review

Mỗi batch nên có ít nhất hai reviewer bản ngữ. Thu thập vùng miền, lĩnh vực và mức quen với domain ở dạng tự nguyện, chỉ dùng để phân tích bias. Khi điểm chênh từ 2 trở lên, giữ cả hai nhận xét và thảo luận nguyên nhân thay vì tự động lấy trung bình.

## Báo cáo

Báo điểm theo skill, domain, register và pattern. Luôn báo số case có blocker riêng. Không quy đổi điểm thành xác suất văn bản do AI tạo. Benchmark nhỏ này phục vụ regression và thảo luận thiết kế, không chứng minh hiệu quả ngoài các domain đã lấy mẫu.
