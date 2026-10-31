**Tiếng Việt** | [English](ROADMAP.md)

# Lộ trình phát triển (Roadmap)

Đã giao đến 0.5.0: bốn skill, linter deterministic, API/frontend, hướng dẫn văn phong và hội thoại, lựa chọn context/giọng khi rewrite, cùng 70 benchmark có 30 case dài theo cặp. Corpus hiện được agent rà soát; đợt tới cần đánh giá độc lập của người bản ngữ và giảm báo nhầm còn lại trước khi thêm pattern.

## Tiếp theo

- Tổ chức đánh giá với người bản ngữ từ nhiều vùng miền và lĩnh vực; lưu vết chỗ chưa thống nhất thay vì áp một đáp án.
- Tiếp tục thêm case `no_change` cho rule dễ bắt nhầm, kèm case thật sự cần sửa của cùng rule.
- Bổ sung glossary theo ngành và fixture nhiều đoạn được reviewer độc lập đánh giá.
- Hiệu chỉnh ngưỡng bằng corpus có giấy phép rõ.

## Sau đó

- Hỗ trợ style guide của dự án qua CLI.
- Thêm baseline từ nhiều mô hình và người đánh giá độc lập.
- Thống kê precision theo pattern, ngành và văn phong.
- Khảo sát văn bản song ngữ và phụ đề.

## 1.0

- Ổn định schema và chính sách phiên bản.
- Công bố benchmark đã đánh giá chéo liên chủ thể.
- Tài liệu tích hợp cho các agent client khác nhau.

*Lộ trình không chứa hạng mục tối ưu hóa để vượt AI detector.*
