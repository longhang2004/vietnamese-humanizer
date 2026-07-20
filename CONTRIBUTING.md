# Đóng góp

Cảm ơn bạn đã giúp bộ công cụ phản ánh tiếng Việt đa dạng hơn.

## Trước khi mở pull request

1. Tìm ID, tên và tín hiệu tương tự trong `docs/generated-patterns.md`.
2. Đọc `docs/pattern-authoring-guide.md`.
3. Ẩn thông tin cá nhân trong ví dụ; không lấy nguyên văn nội dung riêng tư.
4. Thêm hoặc sửa YAML, test hay benchmark và tài liệu liên quan.
5. Chạy `python scripts/generate_pattern_docs.py`.
6. Chạy toàn bộ lệnh kiểm tra trong README.
7. Ghi thay đổi người dùng thấy được vào `CHANGELOG.md`.

## Điều kiện cho pattern mới

Pattern cần lý do rõ, ít nhất hai ví dụ xấu ở ngữ cảnh khác nhau, hai cách sửa hoặc hai output tốt, ngoại lệ, domain, severity, confidence, false-positive risk và test hoặc benchmark. Nêu nguồn quan sát và phản biện trường hợp cấu trúc đó hợp lệ.

Pattern chỉ dựa trên trực giác của một người có thể mở ở dạng proposal để thu thập thêm ví dụ, nhưng chưa nên merge vào catalog stable.

## Quy ước

- ID theo namespace `VI-HUM`, `VI-TRA`, `VI-GRA` hoặc `VI-STY`.
- `name` dùng chữ thường ASCII và dấu gạch nối.
- Tài liệu cho người dùng viết bằng tiếng Việt; identifier và thuật ngữ kỹ thuật có thể giữ tiếng Anh.
- Không thêm score phát hiện AI, claim bypass detector hoặc heuristic có mục đích né kiểm tra.
- Không coi khác biệt vùng miền là lỗi nếu không có ràng buộc register cụ thể.

## Báo lỗi và đánh giá

Dùng issue template phù hợp. Với false positive, cung cấp đoạn tối thiểu còn giữ được ngữ cảnh, domain, register, output mong muốn và lý do pattern hợp lệ ở đó.
