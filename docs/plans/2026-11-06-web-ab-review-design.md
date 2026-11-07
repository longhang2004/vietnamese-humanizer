# Chấm A/B trên web và lưu dữ liệu đánh giá

Ngày: 06/11/2026. Trạng thái: đã triển khai trong source (LON-118/119), backend mặc định tắt cờ `AB_REVIEW_ENABLED`; chưa push/deploy trong các tác vụ QA và UI.

Người dùng đã chọn bản đầu dùng bộ mẫu có sẵn và giấu nhãn hai bản khi chấm. Phần backend dùng SQLAlchemy, cấu hình `DATABASE_URL` và các bảng đóng góp hiện có; bốn bảng và API chấm A/B đã được triển khai theo thiết kế dưới đây.

## Luồng người chấm

- Trang `/review` theo giao diện tối hiện có, chế độ Operate. Mỗi lượt hiện yêu cầu biên tập, đoạn gốc và hai đầu ra nguyên văn mang nhãn A/B. Thứ tự được backend cấp và lưu lại.
- Người đọc chọn A, B, hòa hoặc bỏ qua. Có thể chọn lý do có sẵn: dễ đọc, hợp giọng, giữ đúng ý, hoặc sửa quá tay. Bản đầu dùng các nhãn lý do, chưa mở ô ghi chú tự do.
- Chọn đáp án rồi bấm gửi. Chỉ hiện xác nhận thành công khi database đã commit; khi lỗi, giữ lựa chọn để thử lại. Gửi lại cùng lượt không tạo phiếu trùng.
- Giấu điều kiện có/không nạp skill trong dữ liệu public và giao diện chấm; giữ mapping ở backend. Màn hình hoàn tất báo số lượt đã gửi, giữ riêng số lượt bỏ qua.
- Desktop đặt hai bản cạnh nhau; mobile xếp theo thứ tự A rồi B, giữ đầy đủ nội dung và các lựa chọn có vị trí rõ ràng.

## Lưu trong database backend

Dùng SQLAlchemy và database bền vững qua `DATABASE_URL`; SQLite dành cho phát triển/kiểm thử cục bộ. Dữ liệu đánh giá nằm trong các bảng riêng với đóng góp văn bản.

| Bảng | Nội dung |
| --- | --- |
| `ab_studies` | Mã và phiên bản đợt, trạng thái mở/đóng, mô tả và nguồn bộ mẫu. |
| `ab_cases` | Đợt, chủ đề, profile, input, yêu cầu và hai output cố định; metadata sinh cùng hash nội dung, prompt và snapshot skill. |
| `ab_assignments` | Mã lượt, case, khóa phiên chấm ẩn danh, mapping A/B, thời điểm cấp. |
| `ab_votes` | Mã lượt duy nhất, lựa chọn, điều kiện được chọn do server giải mã, các lý do và thời điểm gửi. |

Output gắn với case vì bản đầu luôn so sánh đúng hai điều kiện. Lưu metadata model/provider/cấu hình khi có; dữ liệu nguồn chưa biết được giữ là chưa biết. Đóng băng case và đầu ra khi mở đợt; thay nội dung hoặc skill phải tạo phiên bản mới.

Backend xác thực case và mapping từ lượt đã cấp; client gửi mã lượt và lựa chọn. Ràng buộc duy nhất và xử lý retry bảo đảm một lượt chỉ có một phiếu. Khóa phiên hỗ trợ hạn chế chấm lặp trong cùng trình duyệt; không được dùng để đếm số người độc lập đã xác minh.

## Query và xuất kết quả

- Query theo study/version, chủ đề, profile, model, snapshot skill và thời gian; tổng hợp số A/B/hòa/bỏ qua, lý do và tỷ lệ chọn từng điều kiện.
- Phân tích cả vị trí trình bày để phát hiện thiên lệch chọn A/B. Lượt bỏ qua có số riêng và được loại khỏi mẫu số tỷ lệ ưu tiên; trường hợp hòa được báo riêng.
- Bản đầu hỗ trợ SQL và công cụ export CSV/JSONL trong môi trường có quyền database. Dashboard quản trị có thể làm sau. Mapping điều kiện và dữ liệu từng lượt không mở qua API public.
- Phiếu mang provenance `anonymous_web`; đợt đánh giá có reviewer độc lập được xác định dùng provenance riêng. Giữ khác biệt này khi xuất hoặc chuyển sang định dạng benchmark hiện có.

## Dữ liệu, vận hành và phạm vi

- Dùng đầu ra AI có bản ghi thật. Sáu cặp đang công khai có thể làm pilot kiểm luồng, được ghi đúng là mẫu công khai; một đợt đánh giá mù mới cần các tình huống giữ lại và đầu ra chưa công bố nhãn.
- Bản đầu phục vụ bộ mẫu có sẵn, không gọi model theo từng lượt. Phiếu chỉ thêm khóa phiên ngẫu nhiên, lựa chọn và nhãn lý do; không thêm trường email, IP hoặc văn bản riêng của người chấm.
- Giữ phiếu, mapping trình bày và bộ mẫu theo từng phiên bản đợt để query, export và đối chiếu lâu dài. Khóa phiên là mã ngẫu nhiên phục vụ hạn chế chấm trùng. Khi mở trang, thông báo rõ lựa chọn được lưu cho việc cải thiện bộ skill; không tự chuyển phiếu thành kết quả benchmark đã xác minh.
- Tính năng có cờ bật riêng, mặc định tắt; giới hạn tần suất theo cơ chế backend hiện có. Nội dung hai output không được render dưới dạng HTML tùy ý.
- Kiểm thử: mapping/order, định dạng phiếu, duplicate/retry, case/study đã đóng, điều kiện bị sửa ở client, quyền export, thống kê hòa/bỏ qua, loading/error, bàn phím và mobile. Dùng database QA riêng cho dữ liệu tổng hợp.

Phần độc lập đã được yêu cầu thực hiện ngay: đồng bộ ROADMAP tiếng Việt/Anh với v0.6.0 và bản web hiện có. Triển khai trang chấm, thêm bảng và mở thu thập là bước tiếp theo sau khi chốt thiết kế này.
