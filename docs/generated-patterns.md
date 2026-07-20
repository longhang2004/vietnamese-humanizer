# Danh mục pattern (được sinh tự động)

> Không sửa trực tiếp file này. Chạy `python scripts/generate_pattern_docs.py` sau khi đổi YAML.

| ID | Skill | Mức độ | Độ tin cậy | Tên | Tóm tắt |
| --- | --- | --- | --- | --- | --- |
| VI-GRA-C01 | grammar-checker-vi | medium | high | `cac-nhung-chong-nhau` | Dùng đồng thời "các" và "những" trước cùng một danh từ mà không có chức năng riêng. |
| VI-GRA-C02 | grammar-checker-vi | low | medium | `boi-vi-cho-nen` | Kết hợp "bởi vì" và "cho nên" trong câu ngắn khi một vế nối đã đủ rõ. |
| VI-GRA-C03 | grammar-checker-vi | medium | low | `tham-chieu-dieu-nay-day-dac` | Lặp "điều này" nhiều lần khi phần được tham chiếu có thể không rõ. |
| VI-GRA-C04 | grammar-checker-vi | medium | low | `dau-phay-tach-chu-vi` | Dấu phẩy có thể đang tách chủ ngữ khỏi vị ngữ mà không có thành phần chen giữa. |
| VI-GRA-L01 | grammar-checker-vi | medium | high | `lap-tu-lien-tiep` | Một từ bị lặp ngay cạnh nhau do lỗi gõ hoặc sửa câu chưa hết. |
| VI-GRA-L02 | grammar-checker-vi | high | high | `chuan-doan-sai-chinh-ta` | Viết "chuẩn đoán" khi nghĩa cần dùng là hoạt động chẩn đoán bệnh hoặc lỗi. |
| VI-GRA-L03 | grammar-checker-vi | medium | high | `sat-nhap-sai-chinh-ta` | Viết "sát nhập" khi nghĩa phổ thông cần dùng là "sáp nhập". |
| VI-GRA-P01 | grammar-checker-vi | medium | high | `khoang-trang-truoc-dau-cau` | Có khoảng trắng thừa trước dấu chấm, phẩy, hỏi, than, hai chấm hoặc chấm phẩy. |
| VI-GRA-P02 | grammar-checker-vi | medium | high | `thieu-khoang-trang-sau-dau-cau` | Thiếu khoảng trắng sau dấu câu khi một từ mới bắt đầu trên cùng dòng. |
| VI-GRA-P03 | grammar-checker-vi | low | medium | `dau-cau-lap` | Lặp nhiều dấu hỏi hoặc dấu than trong văn bản không cần nhấn mạnh cảm xúc. |
| VI-HUM-D01 | humanizer-vi | low | high | `mo-bai-thong-bao-noi-dung` | Mở bài thông báo "trong bài viết này" thay vì đi thẳng vào chủ đề. |
| VI-HUM-D02 | humanizer-vi | low | high | `ket-bai-xa-giao` | Kết thúc bằng lời xã giao chung chung không bổ sung hành động hoặc thông tin. |
| VI-HUM-D03 | humanizer-vi | high | medium | `dan-nguon-mo-ho` | Gán nhận định cho "các chuyên gia" hoặc "nhiều nghiên cứu" mà không xác định nguồn. |
| VI-HUM-L01 | humanizer-vi | medium | medium | `dong-vai-tro-trong-viec` | Lạm dụng cấu trúc "đóng vai trò ... trong việc" khi một động từ trực tiếp rõ hơn. |
| VI-HUM-L02 | humanizer-vi | low | medium | `boi-canh-khong-ngung-phat-trien` | Câu mở bằng "trong bối cảnh không ngừng phát triển" nhưng không nêu thay đổi cụ thể. |
| VI-HUM-L03 | humanizer-vi | medium | medium | `loi-khen-chung-chung` | Dùng nhiều lời khen như "đột phá" hoặc "vượt trội" mà không có căn cứ trong văn bản. |
| VI-HUM-S01 | humanizer-vi | medium | medium | `lap-cau-mo-dau-bang-viec` | Nhiều câu liên tiếp mở bằng "Việc" tạo nhịp đều và che chủ thể thực hiện. |
| VI-HUM-S02 | humanizer-vi | low | medium | `khong-chi-ma-con-lap` | Lặp cấu trúc "không chỉ ... mà còn" để tạo nhấn mạnh cho các ý bình thường. |
| VI-HUM-S03 | humanizer-vi | medium | medium | `tu-noi-day-dac` | Dùng dày các từ nối "đồng thời", "qua đó" và "từ đó" dù quan hệ logic đã rõ. |
| VI-HUM-S04 | humanizer-vi | low | low | `do-dai-cau-dong-deu` | Năm câu trở lên có độ dài gần như nhau, tạo nhịp đều cần người viết đọc lại. |
| VI-STY-C01 | style-guide-vi | low | low | `viet-hoa-danh-tu-chung` | Viết hoa danh từ chung như "Khách Hàng" hoặc "Sản Phẩm" giữa câu để tạo vẻ trang trọng. |
| VI-STY-F01 | style-guide-vi | low | medium | `heading-qua-day` | Dùng nhiều heading cho các phần chỉ có một câu ngắn, làm cấu trúc tài liệu bị vụn. |
| VI-STY-F02 | style-guide-vi | low | medium | `in-dam-co-hoc` | Nhiều bullet mở bằng nhãn in đậm và dấu hai chấm dù nội dung có thể viết thành câu hoặc bảng. |
| VI-STY-N01 | style-guide-vi | low | medium | `don-vi-khong-co-khoang-trang` | Số và ký hiệu đơn vị viết liền trong văn bản khi style dự án yêu cầu một khoảng trắng. |
| VI-STY-N02 | style-guide-vi | low | low | `phan-tram-khong-nhat-quan` | Trộn dạng phần trăm có và không có khoảng trắng trong cùng tài liệu. |
| VI-STY-N03 | style-guide-vi | medium | medium | `ngay-thang-mo-ho` | Ngày viết dạng số ngắn có thể bị hiểu theo thứ tự ngày-tháng hoặc tháng-ngày. |
| VI-STY-P01 | style-guide-vi | medium | medium | `xung-ho-khong-nhat-quan` | Trộn nhiều cách gọi độc giả hoặc người viết mà chưa có lý do chức năng. |
| VI-STY-P02 | style-guide-vi | low | medium | `chung-ta-ep-dong-thuan` | Dùng "chúng ta đều" để trình bày một nhận định như thể người đọc đã đồng ý. |
| VI-STY-T01 | style-guide-vi | low | medium | `login-dang-nhap-lan-lon` | Trộn "login", "log in" và "đăng nhập" cho cùng một thao tác trong nội dung người dùng. |
| VI-STY-T02 | style-guide-vi | low | low | `viet-tat-chua-giai-thich` | Từ viết tắt in hoa xuất hiện trong nội dung phổ thông mà có thể chưa được giải thích. |
| VI-TRA-L01 | translationese-cleaner-vi | medium | high | `mo-khoa-tiem-nang` | Dịch sát "unlock potential" thành "mở khóa tiềm năng" khi ý thực là cho phép hoặc cải thiện một khả năng cụ thể. |
| VI-TRA-L02 | translationese-cleaner-vi | medium | high | `dieu-huong-su-phuc-tap` | Dịch "navigate complexity" thành "điều hướng sự phức tạp" thay vì nêu công việc cần xử lý. |
| VI-TRA-L03 | translationese-cleaner-vi | medium | high | `tac-dong-co-y-nghia` | Dịch "meaningful impact" thành "tác động có ý nghĩa" mà không nêu tác động cụ thể. |
| VI-TRA-L04 | translationese-cleaner-vi | low | high | `o-cap-do-cot-loi` | Dịch "at its core" thành "ở cấp độ cốt lõi" như một lời dẫn tạo vẻ sâu sắc. |
| VI-TRA-L05 | translationese-cleaner-vi | low | medium | `tan-dung-moi-ngu-canh` | Dùng "tận dụng" cho mọi trường hợp của "leverage" dù động từ cụ thể tự nhiên hơn. |
| VI-TRA-L06 | translationese-cleaner-vi | low | medium | `trai-nghiem-lien-mach` | Dịch "seamless experience" thành "trải nghiệm liền mạch" mà không chỉ ra sự gián đoạn được loại bỏ. |
| VI-TRA-S01 | translationese-cleaner-vi | medium | medium | `thong-qua-viec-day-dac` | Lặp "thông qua việc" để dịch cấu trúc "by + V-ing" thay vì dùng động từ trực tiếp. |
| VI-TRA-S02 | translationese-cleaner-vi | medium | high | `thuc-hien-viec` | Dùng động từ nhẹ "thực hiện việc" hoặc "tiến hành thực hiện" trước một hành động rõ. |
| VI-TRA-S03 | translationese-cleaner-vi | medium | low | `bi-dong-che-tac-nhan` | Dùng "được ... bởi" theo tiếng Anh khi tác nhân đã rõ và cần chịu trách nhiệm. |
| VI-TRA-S04 | translationese-cleaner-vi | medium | high | `dua-ra-su-ho-tro` | Dùng "đưa ra/cung cấp sự hỗ trợ" thay cho động từ "hỗ trợ" trong câu thông thường. |

Tổng cộng: **40 pattern**.
