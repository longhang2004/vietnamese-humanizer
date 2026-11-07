**Tiếng Việt** | [English](ROADMAP.md)

# Lộ trình phát triển (Roadmap)

Cập nhật ngày 06/11/2026. Bản phát hành có tag mới nhất là **0.6.0**. Phần triển khai từ `main` được ghi riêng; deploy web không tạo phiên bản phát hành mới.

## Hiện đã có

- Bản 0.6.0 có bốn skill tiếng Việt, 44 quy tắc linter, 103 ví dụ corpus và 124 case benchmark. Sáu nhóm văn phong gồm văn viết rõ ràng, trao đổi công việc, tài liệu kỹ thuật, hành chính, bài đăng mạng xã hội và marketing; mặc định giữ cách viết hiện có. Kênh sử dụng, mức trang trọng, cách xưng hô và mức sửa là các lựa chọn riêng.
- Đã triển khai trình soát theo quy tắc, viết lại bằng AI theo cấu hình dịch vụ, trang `/start`, gói Claude/Gemini, yêu cầu dùng trong chatbot và tài liệu gộp. Gói plugin ChatGPT đã được chuẩn bị; listing công khai, kiểm import trên tài khoản thật và thử với người phổ thông vẫn cần hoàn tất. Xem [hướng dẫn phân phối](docs/user-distribution.md).
- `main` và bản web hiện có landing tối, vùng làm việc `/check`, trang ví dụ, hướng dẫn/giới thiệu, luồng đóng góp theo khả năng backend và sáu cặp đầu ra AI chạy thật. Impeccable 4.8.0 được cài trong repo, kèm format và kiểm tra UI. Các thay đổi này nằm trong mục Unreleased của [changelog](CHANGELOG.vi.md).
- Pilot chấm A/B mù đã có trong source hiện tại: trang `/review` theo khả năng backend, sáu case công khai đóng băng, lượt trình bày mờ có thứ tự A/B được lưu, phiếu bền vững với receipt retry-safe, và CLI summary/CSV/JSONL riêng. Source để `AB_REVIEW_ENABLED=false`; môi trường deploy bật tường minh. Phiếu là phản hồi ẩn danh theo khóa phiên, không phải danh tính reviewer đã xác minh.
- Corpus hiện được agent rà soát, chưa có baseline chất lượng do người đọc độc lập đánh giá. Sáu cặp AI công khai dùng để minh họa hành vi.

## Tiếp theo

- Tổ chức đánh giá độc lập cho sáu nhóm văn phong hiện có theo [quy trình review bản ngữ](benchmarks/profile-review.md). Phân biệt phản hồi ẩn danh trên web với đợt có reviewer độc lập được xác định; lưu cả bất đồng và trường hợp hòa. Pilot chấm A/B mù là đường thu phản hồi ẩn danh; cần thêm case chưa công bố trước khi có thể dùng để kết luận về sở thích.
- Thực hiện [vòng học cùng chủ đề](docs/style-learning-loop.md) trên tình huống chưa thấy. Giữ [pilot bốn biến thể bằng agent](docs/research/2026-11-03-same-topic-pilot.md) riêng khỏi kết quả benchmark; dùng lỗi quan sát được để sửa hướng dẫn của các nhóm văn phong hiện có.
- Tiếp tục thêm case `no_change` cho rule dễ bắt nhầm, kèm case thật sự cần sửa của cùng rule.
- Hiệu chỉnh ngưỡng bằng corpus có giấy phép rõ.
- Hoàn tất kiểm import trên tài khoản thật, thử với 5–10 người không biết code và các bước nộp plugin còn lại trong hướng dẫn phân phối.

## Sau đó

- Hỗ trợ style guide của dự án qua CLI.
- Bổ sung glossary theo ngành và fixture nhiều đoạn được reviewer độc lập đánh giá.
- Thêm baseline từ nhiều mô hình và người đánh giá độc lập.
- Thống kê precision theo pattern, ngành và văn phong khi có dữ liệu đã chấm đủ để ước lượng.
- Đánh giá giọng vui vẻ/hài hước theo lựa chọn, lời nói tự phát, văn bản song ngữ và phụ đề. Hướng dẫn chat và kịch bản nói hiện ở mức thử nghiệm; hành chính, mạng xã hội và marketing đã có profile.

## 1.0

- Ổn định schema và chính sách phiên bản.
- Công bố benchmark đã đánh giá chéo liên chủ thể.
- Tài liệu tích hợp cho các agent client khác nhau.

*Lộ trình không chứa hạng mục tối ưu hóa để vượt AI detector.*
