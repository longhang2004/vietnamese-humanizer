**Tiếng Việt** | [English](ROADMAP.md)

# Lộ trình phát triển (Roadmap)

Đã giao đến 0.5.0: bốn skill, linter deterministic, API/frontend, hướng dẫn văn phong và hội thoại, lựa chọn context/giọng khi rewrite, cùng 70 benchmark có 30 case dài theo cặp. Corpus hiện được agent rà soát; đợt tới cần đánh giá độc lập của người bản ngữ và giảm báo nhầm còn lại trước khi thêm pattern.

## Tiếp theo

- Đã triển khai, chưa phát hành: trang `/start` và gói tải cho người phổ thông. Cần kiểm import trên tài khoản thật, thử với người không biết code và hoàn tất submission plugin ChatGPT theo [hướng dẫn phân phối](docs/user-distribution.md).
- Đã triển khai, chưa phát hành: profile riêng cho văn viết rõ ràng, công việc và kỹ thuật; thêm 24 case theo cặp và báo cáo theo profile/system. Cần [review bản ngữ](benchmarks/profile-review.md) trước khi tuyên bố cải thiện chất lượng.
- Tổ chức đánh giá với người bản ngữ từ nhiều vùng miền và lĩnh vực; lưu vết chỗ chưa thống nhất thay vì áp một đáp án.
- Thực hiện [vòng học cùng chủ đề](docs/style-learning-loop.md) trên tình huống chưa thấy. Đã lưu [pilot bốn biến thể bằng agent](docs/research/2026-11-03-same-topic-pilot.md) riêng khỏi benchmark; ưu tiên nghiên cứu marketing/social, giao tiếp, kịch bản nói và dí dỏm nhẹ theo lựa chọn.
- Tiếp tục thêm case `no_change` cho rule dễ bắt nhầm, kèm case thật sự cần sửa của cùng rule.
- Bổ sung glossary theo ngành và fixture nhiều đoạn được reviewer độc lập đánh giá.
- Hiệu chỉnh ngưỡng bằng corpus có giấy phép rõ.

## Sau đó

- Mở rộng văn bản hành chính và giọng vui vẻ/hài hước theo lựa chọn sau khi đánh giá ba profile đầu.
- Hỗ trợ style guide của dự án qua CLI.
- Thêm baseline từ nhiều mô hình và người đánh giá độc lập.
- Thống kê precision theo pattern, ngành và văn phong.
- Khảo sát văn bản song ngữ và phụ đề.

## 1.0

- Ổn định schema và chính sách phiên bản.
- Công bố benchmark đã đánh giá chéo liên chủ thể.
- Tài liệu tích hợp cho các agent client khác nhau.

*Lộ trình không chứa hạng mục tối ưu hóa để vượt AI detector.*
