# Cách viết trên giao diện web

Giao diện phục vụ người viết tiếng Việt, gồm cả người chưa dùng skill và không viết code. Dùng văn viết rõ ràng, gần gũi; xưng hô với người đọc là “bạn”. Hướng dẫn thao tác cần chính xác về điều kiện và thứ tự bước.

Quy ước này được lập bằng chính các skill của dự án: [humanizer-vi](../skills/humanizer-vi/SKILL.md) với [văn viết rõ ràng](../skills/humanizer-vi/references/plain-writing.md) và [hướng dẫn kỹ thuật](../skills/humanizer-vi/references/technical-writing.md), [style-guide-vi](../skills/style-guide-vi/SKILL.md), [translationese-cleaner-vi](../skills/translationese-cleaner-vi/SKILL.md) và [grammar-checker-vi](../skills/grammar-checker-vi/SKILL.md). Đây là quyết định biên tập của dự án, chưa phải kết quả đánh giá với người dùng thật.

## Quy ước

- Gọi đúng hành động: “Tải skill”, “Sao chép yêu cầu”, “Gửi ví dụ”. Sau thao tác, nói kết quả hoặc cách thử lại nếu đã có cách đó trong sản phẩm.
- Dùng từ quen thuộc và dẫn thẳng tới việc người đọc đang làm. Giải thích một khái niệm khi nó đang cản trở thao tác hoặc khi người đọc tìm phần giải thích; tránh đặt định nghĩa “skill là…” mặc định ở đầu trang.
- Mỗi lời hướng dẫn, lưu ý hoặc phủ định cần giải quyết một vướng mắc cụ thể tại chỗ. Đặt điều kiện cạnh thao tác, giới hạn cạnh kết quả và cách khắc phục sau lỗi. Bỏ phần dẫn thừa được phép biên tập; giữ nguyên điều kiện có tác dụng thật.
- Đặt tên tác vụ nhất quán theo `distribution/catalog.json`. Trang bắt đầu, ô chọn nội dung cần soát và biểu mẫu đóng góp dùng cùng tên. Tên skill trong `SKILL.md`, ID và tên API vẫn là tên kỹ thuật.
- Trong catalog, `summary` mô tả tác vụ cho người dùng; `description` giúp AI chọn skill. Giao diện dùng `summary`, tránh kéo các điều kiện kích hoạt và anti-goals vào phần giới thiệu tác vụ.
- Dùng “văn bản” cho nội dung người đọc đưa vào, “yêu cầu mẫu” cho phần dán vào chatbot, “gợi ý” cho kết quả cần cân nhắc. Không đổi từ chỉ để tránh lặp.
- Giữ nguyên tên sản phẩm và nhãn trên ứng dụng bên ngoài, chẳng hạn `Customize`, `Skills`, `Upload a skill`. Không tự dịch nhãn khiến người đọc khó tìm nút.
- Phân biệt lỗi có căn cứ, chỗ cần xem lại, lựa chọn cách viết và tín hiệu tham khảo. Một dấu hiệu không đủ để gọi câu là sai hoặc khuôn mẫu.
- Không thêm lời đùa, kính ngữ, tiếng lóng hoặc lời hứa như “chính xác tuyệt đối”, “chỉ một bước”. Trạng thái chưa duyệt, chưa phát hành và giới hạn kiểm tra phải rõ.
- Giữ các quy tắc dành cho agent trong tài liệu nội bộ. Nội dung mặc định trên web tập trung vào tác vụ; thông tin về phạm vi công cụ có thể đặt trong mục mở rộng, thay vì lặp lời phủ định ở đầu và cuối mọi trang.
- Giữ nguyên số liệu, giới hạn nhập, phạm vi đồng ý chia sẻ, URL, mã và giá trị gửi API. Biên tập câu chữ không mở rộng quyền thu thập dữ liệu hay thay đổi chức năng.

## Ví dụ đã áp dụng

| Trước | Sau | Lý do |
| --- | --- | --- |
| Gọt dịch thuật ngữ tiếng Việt | Sửa câu dịch chưa tự nhiên | Gọi đúng việc sửa cấu trúc dịch sát, không gợi ý thay thuật ngữ. |
| Quy chuẩn văn phong & báo chí | Giữ cách viết nhất quán | Không khiến người đọc hiểu skill chỉ dành cho báo chí hoặc có một chuẩn bắt buộc. |
| Đóng góp ví dụ / Case văn phong | Góp ví dụ biên tập tiếng Việt | Nêu việc người đọc có thể làm. |
| Lối viết khuôn mẫu | Tín hiệu tham khảo | Giữ tính gợi ý của phát hiện heuristic. |

## Rà trước khi push

Đọc cả luồng từ chọn tác vụ tới kết quả, rồi đối chiếu điều kiện và giới hạn với mã xử lý. Chạy lại exporter nếu đổi catalog. Kiểm tra nhãn, câu báo lỗi, phần trống, metadata và bố cục ở màn hình nhỏ; giữ câu đã rõ.
