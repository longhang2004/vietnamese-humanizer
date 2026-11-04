# Đọc bổ sung nguồn tiếng Việt

Ngày đọc: 04-11-2026, tiếp sau khảo sát [nguồn quốc tế](2026-11-04-formulaic-prose.md). Đợt trước chưa khảo sát nguồn Việt đủ sâu. Đợt này đọc bài gốc, blog nghề viết và diễn đàn; ghi riêng ngày công bố, điều quan sát được và phần chưa có kiểm chứng.

## Nguồn đã đọc

| Nguồn | Ngày và cách đọc | Điều dùng được / giới hạn |
| --- | --- | --- |
| Phạm Mỹ, Báo Văn Nghệ — [“Mùi” AI](https://baovannghe.vn/mui-ai-26802.html) | 23-02-2026; đọc HTML | Người làm nội dung nhận xét các khuôn lặp trong thiệp, lời chúc và bài thương mại. Dùng để xét sự đồng dạng theo ngữ cảnh Việt; các khẳng định về cơ chế model và khả năng xác định tác giả trong bài chưa được dự án kiểm chứng. |
| Upcontent — [Kiểm tra văn bản AI: công cụ, độ chính xác và cách sửa văn máy](https://upcontent.vn/kiem-tra-van-ban-ai/) | 23-10-2026 trên trang; công cụ đọc web bị cache miss, đã đọc bài qua trình duyệt | Phép thử thay tên thương hiệu giúp tìm nội dung thiếu chi tiết riêng. Dùng dữ kiện được cung cấp để biên tập hoặc hỏi thêm khi cần. Nguồn có bán dịch vụ; không áp danh sách từ cấm hay chỉ tiêu mỗi đoạn phải có một chi tiết. |
| Hoà Lương — [Hiểu về dấu gạch ngang để không còn hoang mang](https://hoaluong.com/hieu-ve-dau-gach-ngang-de-khong-con-hoang-mang/) | Chưa xác minh ngày công bố; công cụ đọc web bị cache miss, đã đọc qua trình duyệt | Tình huống sửa câu và phân biệt chức năng dấu câu. Tham khảo việc giữ lượt thoại, phần chú thích và tổ hợp tên/số; không áp lệnh xóa một ký tự Unicode hay coi bài blog là tiêu chuẩn chính thức cho mọi quy ước trình bày. |
| `theghostofyou` và người bình luận, VOZ — [Cảm thấy khó chịu với content từ AI](https://voz.vn/t/cam-thay-kho-chiu-voi-content-tu-ai.1104978/) | Bắt đầu 26-05-2025; đọc trang 1, gồm phản hồi 27-05 | Phản hồi về nội dung dài mà ít ích lợi, văn SEO na ná và quảng cáo chen vào trả lời. Nhiều bình luận bàn về ảnh/video; chỉ dùng phần liên quan tới văn bản, không xem cảm giác của tài khoản là bộ nhận diện. |
| Pnghuy, Tinh tế — [Trải nghiệm Samsung One UI 6.1 trên Galaxy S23](https://tinhte.vn/thread/trai-nghiem-samsung-one-ui-6-1-tren-galaxy-s23.3774246/) | 30-03-2024; đọc mục “Kiểu viết” và ngữ cảnh bài | Trải nghiệm trực tiếp cho rằng các preset vẫn giữ một bố cục, chỉ đổi từ. Bài cũ, giới hạn ở tính năng được thử lúc đó; dùng làm câu hỏi rà bản sửa, không suy ra chất lượng model hiện nay. |
| Ban biên tập Finhay — [Mẹo dùng ChatGPT không bị văn mẫu](https://www.finhay.com.vn/meo-dung-chatgpt-khong-bi-van-mau-robotic) | 29-05-2026; đọc HTML | Có gợi ý cung cấp mẫu giọng và trải nghiệm thật. Không áp tỷ lệ nhận diện chưa được kiểm chứng, mẹo tự thêm tiếng lóng, câu cực ngắn hay dấu câu để gây cảm giác giống người. |

Các trang tiếng Việt dịch hoặc tổng hợp thảo luận nước ngoài không được tính thành quan sát độc lập tại Việt Nam. Tên tác giả/tài khoản là thông tin quy nguồn, chưa chứng nhận quá trình viết từng câu.

## Vận dụng

Bổ sung vào [reference lối viết theo khuôn](../../skills/humanizer-vi/references/formulaic-prose.md):

- Rà phần dẫn và lời tôn vinh có thể hoán đổi giữa nhiều thiệp, lời chúc, bài tri ân. Giữ ẩn dụ của người viết khi có dụng ý; quyền bỏ lời bình vẫn phải rõ.
- Dùng phép thử thay tên như câu hỏi về nội dung riêng trong bài giới thiệu/review, không coi nó là phép thử nguồn gốc. Văn bản theo mẫu hoặc hướng dẫn chung có thể cần giống nhau. Thiếu thông tin riêng thì hỏi/góp ý, không bịa giá, khách hàng hoặc trải nghiệm.
- Xét dấu gạch ngang theo chức năng câu và quy ước của người viết. Giữ đối thoại, chú thích và khoảng số phù hợp; sửa mạch câu nếu phần chen ngang làm khó đọc.
- Khi đổi giọng, kiểm cả cách tổ chức ý. Việc thay một vài tính từ không đủ để kết luận đã phù hợp; bài vốn đúng được giữ nguyên. Tiếng lóng, xưng hô vùng miền và chi tiết cá nhân chỉ dùng khi có căn cứ hoặc yêu cầu.

Ví dụ bổ sung trong reference do dự án tự viết. Giữ 44 pattern và 106 benchmark case; đợt này chưa thêm regex, chưa có đo cải thiện hoặc đánh giá bản ngữ độc lập.
