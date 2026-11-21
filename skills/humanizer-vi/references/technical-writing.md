# Tài liệu kỹ thuật — `profile=technical`

Trước khi sửa, xác định văn bản là hướng dẫn thao tác, giải thích khái niệm, tài liệu tham chiếu, ghi chú thay đổi, báo cáo phân tích hay bài nghiên cứu. Giữ bố cục phù hợp với loại tài liệu. Chỉ trình bày thành các bước khi người đọc cần làm theo trình tự.

Xác định kiến thức tiền đề từ audience/context: người dùng mới và developer đã biết nền tảng cần mức giải thích khác nhau. Giải thích khái niệm ở nơi nó giúp hiểu hoặc thực hiện bước hiện tại; tránh tự thêm phần nhập môn chỉ vì tài liệu có thuật ngữ. Giữ định nghĩa tác giả đã chủ ý đặt. Nguồn tiếng Việt của ZaloPay ở [sources](sources.md) minh họa cách công bố đối tượng trước khi đi vào nội dung nâng cao.

## Quyết định biên tập

- **Hướng dẫn thao tác:** làm rõ điều kiện áp dụng, hành động và kết quả đã được mô tả. Giữ thứ tự phụ thuộc; đặt cảnh báo trước thao tác liên quan khi được sắp xếp lại. Không tự thêm bước hay lệnh để quy trình có vẻ hoàn chỉnh.
- Nếu nguồn đã cho một trạng thái hoặc thông báo để biết khi nào có thể đi tiếp, đặt nó cạnh hành động phải chờ. Diễn đạt điều người đọc có thể làm tại chỗ, rồi nêu hậu quả của việc làm sớm nếu nguồn có. Giữ đúng phạm vi và mức chắc chắn của cảnh báo. Nếu hành động chỉ là tùy chọn, giữ cách diễn đạt cho biết người đọc có thể chọn và tránh biến nó thành bước kế tiếp.
- **Tài liệu tham chiếu:** đi thẳng vào chức năng, tham số, giá trị trả về và giới hạn đã có. Giữ ngắn gọn, cho phép cấu trúc lặp giúp tra cứu.
- **Giải thích khái niệm:** giữ thuật ngữ nhất quán và nối nguyên nhân–cơ chế–hệ quả theo bằng chứng trong input/context. Không tự thêm cơ chế hoặc ví dụ thực thi.
- **Ghi chú thay đổi:** phân biệt hành vi trước/sau, phiên bản và phạm vi ảnh hưởng. Không biến một thay đổi cho nhóm thử nghiệm thành thay đổi cho mọi tài khoản.
- Giữ code, tên API, identifier, URL, path, nhãn UI, số, đơn vị và thứ tự tham số. Không Việt hóa hay đổi hoa/thường các token đó để câu “mượt” hơn.
- Theo glossary được duyệt. Giữ tiếng Anh khi đó là thuật ngữ của sản phẩm hoặc cộng đồng; giải thích bằng dữ kiện sẵn có khi đối tượng là người mới. Nếu chưa biết hai từ có cùng nghĩa hay không, hỏi thay vì gộp.
- Giữ chính xác “chỉ khi”, “trừ khi”, “không”, “mặc định”, “tối đa”, “ít nhất” và “có thể”. Không làm nhẹ cảnh báo hoặc nâng bảo đảm.
- Giọng thân thiện có thể trực tiếp và dễ hiểu. Tránh tự thêm “rất đơn giản”, “chỉ cần”, lời đùa hoặc lời khen sản phẩm. Giữ mức trang trọng người dùng đã chọn.

## Báo cáo phân tích và nghiên cứu

- Mở đoạn bằng đối tượng đang xét hoặc phát hiện cần đọc nếu mức sửa cho phép. Nối câu sau với chỉ số, đối tượng hoặc ý vừa nêu. Lặp đúng thuật ngữ khi việc đó giúp người đọc biết các câu đang nói về cùng một thứ.
- Theo mẫu của nơi nhận hoặc tạp chí. Phần kết quả nêu điều quan sát hoặc đo được và dẫn đến bảng, hình liên quan. Phần thảo luận giải thích ý nghĩa và giới hạn dựa trên bằng chứng. Khi hai phần cùng một mục, vẫn giữ rõ vai trò của từng câu. Giữ số bảng, hình và trích dẫn đúng chỗ.
- Đặt kỳ số liệu, mốc so sánh, đơn vị, mẫu số, đối tượng khảo sát và điều kiện đo cạnh kết quả liên quan. Giữ mức “sơ bộ” hay “ước tính”, phân biệt phần trăm với điểm phần trăm và giữ nguyên số liệu về độ bất định đã có. Khi bảng nguồn có sẵn và được phép rút gọn, chọn số cần cho nhận xét chính.
- Giữ mức kết luận mà dữ liệu cho phép. “Chưa phát hiện khác biệt có ý nghĩa thống kê” mô tả kết quả phân tích. Kết luận hai nhóm tương đương cần bằng chứng riêng. Giữ ranh giới của mô phỏng và khảo sát quan sát. Nếu bản gốc có kết luận vượt quá bằng chứng đã cho, góp ý ở đúng câu và chờ tác giả xác nhận trước khi thay luận điểm.
- Trong nghiên cứu định tính, gắn nhận định với dữ liệu như lời kể, ghi chép hoặc nhóm chủ đề. Giữ rõ đâu là lời người tham gia và đâu là diễn giải của tác giả. Giữ nguyên lời trích trực tiếp và mã người tham gia theo bản gốc. Giữ phạm vi của “một số”, “trong các cuộc phỏng vấn” và các cách chỉ nhóm tương tự.

## Ví dụ tự viết, chưa được người bản ngữ duyệt

**Sửa cục bộ:**

Input: “Trong trường hợp mã phản hồi là `429`, việc thử lại yêu cầu cần được thực hiện sau ít nhất 30 giây. Việc thử lại không được thực hiện tự động với yêu cầu `POST`.”

Gợi ý: “Nếu mã phản hồi là `429`, hãy đợi ít nhất 30 giây trước khi thử lại yêu cầu. Không tự động thử lại yêu cầu `POST`.”

Lý do: làm rõ điều kiện và thao tác, giữ giới hạn tối thiểu và lệnh cấm. Không suy ra mọi `POST` đều an toàn để thử lại thủ công.

**Đặt mốc chờ:** Giữ cửa sổ mở đến khi thấy “Đã lưu”. Đóng sớm có thể làm gián đoạn việc lưu. Khi cần, bạn có thể bấm “Xem bản lưu”. Dùng cách này khi nguồn có đủ thông báo, rủi ro và nút tùy chọn. Lời dặn chờ cần giúp người đọc tiếp tục thao tác tại cửa sổ đó.

**Giữ nguyên:** “`get_status(id)` trả về `null` nếu không tìm thấy tác vụ. Hàm không tạo tác vụ mới.” Cấu trúc trực tiếp hợp tài liệu tham chiếu; không cần mở đầu “Hãy cùng tìm hiểu”.

**Cần tác giả quyết định:** “Xóa thư mục cũ rồi chạy lại lệnh trên.” Nếu người dùng cần hướng dẫn thực thi độc lập, phải hỏi đường dẫn và lệnh cụ thể. Không tự thêm `rm -rf`, đoán thư mục hay điền lệnh từ kiến thức ngoài bài.

**Rút lời dẫn khảo sát.** “Qua quá trình tiến hành khảo sát, kết quả thu được cho thấy rằng 38 trong số 120 người tham gia cho biết gặp khó khăn khi nộp hồ sơ” có thể viết thành “Trong 120 người được khảo sát, 38 người cho biết gặp khó khăn khi nộp hồ sơ.” Giữ mẫu số và cách quy nguồn cho người trả lời.

## Rà cuối

Người làm theo có thấy điều kiện và cảnh báo trước khi hành động không? Token và đơn vị có còn nguyên không? Có đổi thao tác tùy chọn thành bắt buộc hoặc tạo bảo đảm mới không? Với báo cáo, người đọc có thấy kết quả đo trong điều kiện nào và tác giả diễn giải đến đâu không? Nếu đã rõ, chọn `no_change`.

Nguồn về giọng tài liệu developer, quy trình, báo cáo và nghiên cứu được ghi trong [ghi chú nguồn](sources.md). Nguyên tắc tiếng Anh được chọn lọc theo mục đích; các quyết định tiếng Việt trên còn cần review độc lập.
