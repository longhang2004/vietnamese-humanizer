# Tài liệu kỹ thuật — `profile=technical`

Xác định trước đây là hướng dẫn thao tác, giải thích khái niệm, tài liệu tham chiếu hay ghi chú thay đổi. Mỗi loại có cách tổ chức riêng; không biến mọi đoạn thành các bước đánh số.

Xác định kiến thức tiền đề từ audience/context: người dùng mới và developer đã biết nền tảng cần mức giải thích khác nhau. Không tự thêm phần nhập môn hoặc xóa định nghĩa tác giả đã chủ ý giữ. Nguồn tiếng Việt của ZaloPay ở [sources](sources.md) minh họa cách công bố đối tượng trước khi đi vào nội dung nâng cao.

## Quyết định biên tập

- **Hướng dẫn thao tác:** làm rõ điều kiện áp dụng, hành động và kết quả đã được mô tả. Giữ thứ tự phụ thuộc; đặt cảnh báo trước thao tác liên quan khi được sắp xếp lại. Không tự thêm bước hay lệnh để quy trình có vẻ hoàn chỉnh.
- **Tài liệu tham chiếu:** đi thẳng vào chức năng, tham số, giá trị trả về và giới hạn đã có. Giữ ngắn gọn, cho phép cấu trúc lặp giúp tra cứu.
- **Giải thích khái niệm:** giữ thuật ngữ nhất quán và nối nguyên nhân–cơ chế–hệ quả theo bằng chứng trong input/context. Không tự thêm cơ chế hoặc ví dụ thực thi.
- **Ghi chú thay đổi:** phân biệt hành vi trước/sau, phiên bản và phạm vi ảnh hưởng. Không biến một thay đổi cho nhóm thử nghiệm thành thay đổi cho mọi tài khoản.
- Giữ code, tên API, identifier, URL, path, nhãn UI, số, đơn vị và thứ tự tham số. Không Việt hóa hay đổi hoa/thường các token đó để câu “mượt” hơn.
- Theo glossary được duyệt. Giữ tiếng Anh khi đó là thuật ngữ của sản phẩm hoặc cộng đồng; giải thích bằng dữ kiện sẵn có khi đối tượng là người mới. Nếu chưa biết hai từ có cùng nghĩa hay không, hỏi thay vì gộp.
- Giữ chính xác “chỉ khi”, “trừ khi”, “không”, “mặc định”, “tối đa”, “ít nhất” và “có thể”. Không làm nhẹ cảnh báo hoặc nâng bảo đảm.
- Giọng thân thiện có thể trực tiếp và dễ hiểu. Tránh tự thêm “rất đơn giản”, “chỉ cần”, lời đùa hoặc lời khen sản phẩm. Giữ mức trang trọng người dùng đã chọn.

## Ví dụ tự viết, chưa được người bản ngữ duyệt

**Sửa cục bộ:**

Input: “Trong trường hợp mã phản hồi là `429`, việc thử lại yêu cầu cần được thực hiện sau ít nhất 30 giây. Việc thử lại không được thực hiện tự động với yêu cầu `POST`.”

Gợi ý: “Nếu mã phản hồi là `429`, hãy đợi ít nhất 30 giây trước khi thử lại yêu cầu. Không tự động thử lại yêu cầu `POST`.”

Lý do: làm rõ điều kiện và thao tác, giữ giới hạn tối thiểu và lệnh cấm. Không suy ra mọi `POST` đều an toàn để thử lại thủ công.

**Giữ nguyên:** “`get_status(id)` trả về `null` nếu không tìm thấy tác vụ. Hàm không tạo tác vụ mới.” Cấu trúc trực tiếp hợp tài liệu tham chiếu; không cần mở đầu “Hãy cùng tìm hiểu”.

**Cần tác giả quyết định:** “Xóa thư mục cũ rồi chạy lại lệnh trên.” Nếu người dùng cần hướng dẫn thực thi độc lập, phải hỏi đường dẫn và lệnh cụ thể. Không tự thêm `rm -rf`, đoán thư mục hay điền lệnh từ kiến thức ngoài bài.

## Rà cuối

Người làm theo có thấy điều kiện và cảnh báo trước khi hành động không? Token và đơn vị có còn nguyên không? Có đổi thao tác tùy chọn thành bắt buộc hoặc tạo bảo đảm mới không? Nếu đã rõ, chọn `no_change`.

Nguồn về giọng tài liệu developer và cách viết quy trình được ghi ở [sources](sources.md). Nguyên tắc tiếng Anh được chọn lọc theo mục đích; các quyết định tiếng Việt trên còn cần review độc lập.
