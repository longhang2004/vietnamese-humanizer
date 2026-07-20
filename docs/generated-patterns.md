# Danh mục pattern (được sinh tự động)

> Không sửa trực tiếp file này. Chạy `python scripts/generate_pattern_docs.py` sau khi đổi YAML.

## VI-GRA-C01: `cac-nhung-chong-nhau`

- Skill: `grammar-checker-vi`
- Finding type: `error`
- Scope / aggregation: `phrase` / `single`
- Severity / confidence: `medium` / `high`
- False-positive risk: `low`
- Tóm tắt: Dùng đồng thời "các" và "những" trước cùng một danh từ mà không có chức năng riêng.
- Rewrite strategy:
  - Giữ "các" cho tập xác định hoặc "những" cho một số phần tử tùy ý nghĩa.
- Exceptions:
  - Nội dung trích dẫn nguyên văn hoặc đang phân tích chính lỗi này.

## VI-GRA-C02: `boi-vi-cho-nen`

- Skill: `grammar-checker-vi`
- Finding type: `preference`
- Scope / aggregation: `sentence` / `count`
- Severity / confidence: `low` / `medium`
- False-positive risk: `high`
- Tóm tắt: Kết hợp "bởi vì" và "cho nên" trong câu ngắn khi một vế nối đã đủ rõ.
- Rewrite strategy:
  - Giữ một đầu nối khi câu viết cần gọn; giữ cả hai nếu nhịp nói hoặc cấu trúc dài cần đánh dấu.
- Exceptions:
  - Văn nói, lời thoại, câu dài cần đánh dấu rõ hai vế hoặc phong cách tác giả.

## VI-GRA-C03: `tham-chieu-dieu-nay-day-dac`

- Skill: `grammar-checker-vi`
- Finding type: `warning`
- Scope / aggregation: `paragraph` / `count`
- Severity / confidence: `medium` / `low`
- False-positive risk: `high`
- Tóm tắt: Lặp "điều này" nhiều lần khi phần được tham chiếu có thể không rõ.
- Rewrite strategy:
  - Gọi tên sự việc được tham chiếu khi có hơn một tiền tố hợp lý; nếu chưa rõ thì hỏi tác giả.
- Exceptions:
  - Khi câu trước chỉ có một mệnh đề và tham chiếu không thể hiểu theo cách khác.

## VI-GRA-C04: `dau-phay-tach-chu-vi`

- Skill: `grammar-checker-vi`
- Finding type: `heuristic`
- Scope / aggregation: `sentence` / `single`
- Severity / confidence: `medium` / `low`
- False-positive risk: `high`
- Tóm tắt: Dấu phẩy có thể đang tách chủ ngữ khỏi vị ngữ mà không có thành phần chen giữa.
- Rewrite strategy:
  - Đọc cấu trúc câu; xóa dấu phẩy chỉ khi không có mệnh đề hoặc thành phần chen hợp lệ.
- Exceptions:
  - Khi giữa chủ ngữ và vị ngữ có thành phần chen, chú thích hoặc mệnh đề phụ.

## VI-GRA-L01: `lap-tu-lien-tiep`

- Skill: `grammar-checker-vi`
- Finding type: `error`
- Scope / aggregation: `token` / `single`
- Severity / confidence: `medium` / `high`
- False-positive risk: `low`
- Tóm tắt: Một từ bị lặp ngay cạnh nhau do lỗi gõ hoặc sửa câu chưa hết.
- Rewrite strategy:
  - Xóa một lần lặp sau khi chắc hai từ không thuộc cấu trúc nhấn mạnh có chủ đích.
- Exceptions:
  - Phép lặp biểu cảm, lời thoại, thơ hoặc ví dụ đang phân tích chính từ đó.

## VI-GRA-L02: `chuan-doan-sai-chinh-ta`

- Skill: `grammar-checker-vi`
- Finding type: `error`
- Scope / aggregation: `token` / `single`
- Severity / confidence: `high` / `high`
- False-positive risk: `low`
- Tóm tắt: Viết "chuẩn đoán" khi nghĩa cần dùng là hoạt động chẩn đoán bệnh hoặc lỗi.
- Rewrite strategy:
  - Đổi thành "chẩn đoán" khi nói đến việc xác định bệnh, tình trạng hoặc nguyên nhân lỗi.
- Exceptions:
  - Trích dẫn nguyên văn, tên riêng hoặc nội dung đang minh họa lỗi chính tả.

## VI-GRA-L03: `sat-nhap-sai-chinh-ta`

- Skill: `grammar-checker-vi`
- Finding type: `error`
- Scope / aggregation: `token` / `single`
- Severity / confidence: `medium` / `high`
- False-positive risk: `low`
- Tóm tắt: Viết "sát nhập" khi nghĩa phổ thông cần dùng là "sáp nhập".
- Rewrite strategy:
  - Đổi thành "sáp nhập" nếu không phải tên riêng hoặc trích dẫn.
- Exceptions:
  - Tên tác phẩm, trích dẫn hoặc dữ liệu cần giữ nguyên chính tả nguồn.

## VI-GRA-P01: `khoang-trang-truoc-dau-cau`

- Skill: `grammar-checker-vi`
- Finding type: `error`
- Scope / aggregation: `token` / `single`
- Severity / confidence: `medium` / `high`
- False-positive risk: `low`
- Tóm tắt: Có khoảng trắng thừa trước dấu chấm, phẩy, hỏi, than, hai chấm hoặc chấm phẩy.
- Rewrite strategy:
  - Xóa khoảng trắng trước dấu câu, trừ khi nội dung thuộc code hoặc dữ liệu đặc thù.
- Exceptions:
  - Code, biểu thức, dữ liệu nguyên bản hoặc style typography chuyên biệt.

## VI-GRA-P02: `thieu-khoang-trang-sau-dau-cau`

- Skill: `grammar-checker-vi`
- Finding type: `error`
- Scope / aggregation: `token` / `single`
- Severity / confidence: `medium` / `high`
- False-positive risk: `medium`
- Tóm tắt: Thiếu khoảng trắng sau dấu câu khi một từ mới bắt đầu trên cùng dòng.
- Rewrite strategy:
  - Thêm một khoảng trắng sau dấu câu nếu đây không phải số, URL, code hay viết tắt.
- Exceptions:
  - Số thập phân, URL, email, phiên bản, code và identifier.

## VI-GRA-P03: `dau-cau-lap`

- Skill: `grammar-checker-vi`
- Finding type: `preference`
- Scope / aggregation: `token` / `single`
- Severity / confidence: `low` / `medium`
- False-positive risk: `high`
- Tóm tắt: Lặp nhiều dấu hỏi hoặc dấu than trong văn bản không cần nhấn mạnh cảm xúc.
- Rewrite strategy:
  - Giữ một dấu; nếu cảm xúc có chủ đích trong mạng xã hội thì để nguyên.
- Exceptions:
  - Hội thoại, mạng xã hội, trích dẫn và văn chương dùng dấu lặp có chủ đích.

## VI-HUM-D01: `mo-bai-thong-bao-noi-dung`

- Skill: `humanizer-vi`
- Finding type: `preference`
- Scope / aggregation: `document` / `single`
- Severity / confidence: `low` / `high`
- False-positive risk: `low`
- Tóm tắt: Mở bài thông báo "trong bài viết này" thay vì đi thẳng vào chủ đề.
- Rewrite strategy:
  - Mở bằng vấn đề, kết luận chính hoặc bối cảnh cụ thể.
- Exceptions:
  - Trong syllabus, proposal hoặc tài liệu dài cần nêu rõ phạm vi và cấu trúc.

## VI-HUM-D02: `ket-bai-xa-giao`

- Skill: `humanizer-vi`
- Finding type: `preference`
- Scope / aggregation: `document` / `single`
- Severity / confidence: `low` / `high`
- False-positive risk: `low`
- Tóm tắt: Kết thúc bằng lời xã giao chung chung không bổ sung hành động hoặc thông tin.
- Rewrite strategy:
  - Kết ở thông tin cuối cùng hoặc nêu bước tiếp theo có thật.
- Exceptions:
  - Trong thư cá nhân hoặc trao đổi chăm sóc khách hàng khi lời chúc phù hợp quan hệ.

## VI-HUM-D03: `dan-nguon-mo-ho`

- Skill: `humanizer-vi`
- Finding type: `warning`
- Scope / aggregation: `sentence` / `single`
- Severity / confidence: `high` / `medium`
- False-positive risk: `medium`
- Tóm tắt: Gán nhận định cho "các chuyên gia" hoặc "nhiều nghiên cứu" mà không xác định nguồn.
- Rewrite strategy:
  - Nêu nguồn có sẵn; nếu không có, thu hẹp tuyên bố hoặc đánh dấu cần nguồn.
- Exceptions:
  - Khi nguồn đã được nêu rõ ở câu ngay trước và cụm này chỉ tham chiếu lại.

## VI-HUM-L01: `dong-vai-tro-trong-viec`

- Skill: `humanizer-vi`
- Finding type: `heuristic`
- Scope / aggregation: `phrase` / `density`
- Severity / confidence: `medium` / `medium`
- False-positive risk: `medium`
- Tóm tắt: Lạm dụng cấu trúc "đóng vai trò ... trong việc" khi một động từ trực tiếp rõ hơn.
- Rewrite strategy:
  - Xác định hành động thật rồi đưa động từ đó lên làm vị ngữ chính.
  - Giữ mức độ quan trọng nếu văn bản có căn cứ cho đánh giá ấy.
- Exceptions:
  - Khi văn bản thực sự phân tích vai trò của một người, bộ phận hoặc chức năng.

## VI-HUM-L02: `boi-canh-khong-ngung-phat-trien`

- Skill: `humanizer-vi`
- Finding type: `heuristic`
- Scope / aggregation: `paragraph` / `density`
- Severity / confidence: `low` / `medium`
- False-positive risk: `medium`
- Tóm tắt: Câu mở bằng "trong bối cảnh không ngừng phát triển" nhưng không nêu thay đổi cụ thể.
- Rewrite strategy:
  - Nêu thay đổi, mốc thời gian hoặc áp lực cụ thể; nếu không có thì bỏ lời dẫn.
- Exceptions:
  - Khi câu sau định nghĩa rõ xu hướng và lời dẫn giúp liên kết với đoạn trước.

## VI-HUM-L03: `loi-khen-chung-chung`

- Skill: `humanizer-vi`
- Finding type: `warning`
- Scope / aggregation: `paragraph` / `density`
- Severity / confidence: `medium` / `medium`
- False-positive risk: `medium`
- Tóm tắt: Dùng nhiều lời khen như "đột phá" hoặc "vượt trội" mà không có căn cứ trong văn bản.
- Rewrite strategy:
  - Thay lời khen bằng đặc tính, kết quả hoặc bằng chứng đã có trong đầu vào.
- Exceptions:
  - Khi đây là trích dẫn, slogan đã duyệt hoặc lời đánh giá có nguồn và tiêu chí rõ.

## VI-HUM-S01: `lap-cau-mo-dau-bang-viec`

- Skill: `humanizer-vi`
- Finding type: `heuristic`
- Scope / aggregation: `paragraph` / `sequence`
- Severity / confidence: `medium` / `medium`
- False-positive risk: `medium`
- Tóm tắt: Nhiều câu liên tiếp mở bằng "Việc" tạo nhịp đều và che chủ thể thực hiện.
- Rewrite strategy:
  - Đưa chủ thể hoặc động từ lên đầu; gộp câu khi chúng cùng một chủ thể.
- Exceptions:
  - Khi "việc" gọi tên một hành vi đã được định nghĩa trong văn bản pháp lý hoặc phân tích.

## VI-HUM-S02: `khong-chi-ma-con-lap`

- Skill: `humanizer-vi`
- Finding type: `heuristic`
- Scope / aggregation: `paragraph` / `count`
- Severity / confidence: `low` / `medium`
- False-positive risk: `high`
- Tóm tắt: Lặp cấu trúc "không chỉ ... mà còn" để tạo nhấn mạnh cho các ý bình thường.
- Rewrite strategy:
  - Nêu trực tiếp hai tác động hoặc chọn tác động quan trọng hơn.
- Exceptions:
  - Khi phép đối sánh là trọng tâm lập luận và không bị lặp trong đoạn.

## VI-HUM-S03: `tu-noi-day-dac`

- Skill: `humanizer-vi`
- Finding type: `heuristic`
- Scope / aggregation: `paragraph` / `density`
- Severity / confidence: `medium` / `medium`
- False-positive risk: `medium`
- Tóm tắt: Dùng dày các từ nối "đồng thời", "qua đó" và "từ đó" dù quan hệ logic đã rõ.
- Rewrite strategy:
  - Giữ từ nối chỉ khi nó diễn đạt quan hệ logic cần thiết; tách câu nếu có quá nhiều mệnh đề.
- Exceptions:
  - Trong lập luận dài khi mỗi từ nối biểu thị một quan hệ khác nhau và chính xác.

## VI-HUM-S04: `do-dai-cau-dong-deu`

- Skill: `humanizer-vi`
- Finding type: `heuristic`
- Scope / aggregation: `document` / `variance`
- Severity / confidence: `low` / `low`
- False-positive risk: `high`
- Tóm tắt: Năm câu trở lên có độ dài gần như nhau, tạo nhịp đều cần người viết đọc lại.
- Rewrite strategy:
  - Đọc thành tiếng và chỉ tách hoặc gộp nơi cấu trúc ý cần thay đổi.
- Exceptions:
  - Checklist, thông số kỹ thuật, văn bản cho người mới đọc hoặc nhịp lặp có chủ đích.

## VI-STY-C01: `viet-hoa-danh-tu-chung`

- Skill: `style-guide-vi`
- Finding type: `preference`
- Scope / aggregation: `token` / `single`
- Severity / confidence: `low` / `low`
- False-positive risk: `high`
- Tóm tắt: Viết hoa danh từ chung như "Khách Hàng" hoặc "Sản Phẩm" giữa câu để tạo vẻ trang trọng.
- Rewrite strategy:
  - Viết thường danh từ chung, trừ tên riêng, thuật ngữ pháp lý đã định nghĩa hoặc style thương hiệu.
- Exceptions:
  - Tên thương hiệu, nhãn UI, thuật ngữ đã định nghĩa trong hợp đồng hoặc style guide yêu cầu.

## VI-STY-F01: `heading-qua-day`

- Skill: `style-guide-vi`
- Finding type: `heuristic`
- Scope / aggregation: `document` / `density`
- Severity / confidence: `low` / `medium`
- False-positive risk: `high`
- Tóm tắt: Dùng nhiều heading cho các phần chỉ có một câu ngắn, làm cấu trúc tài liệu bị vụn.
- Rewrite strategy:
  - Gộp các mục cùng chủ đề thành đoạn hoặc danh sách; giữ heading khi nó giúp điều hướng tài liệu dài.
- Exceptions:
  - Reference tra cứu nhanh, FAQ, UI copy inventory hoặc cấu trúc do hệ thống sinh.

## VI-STY-F02: `in-dam-co-hoc`

- Skill: `style-guide-vi`
- Finding type: `heuristic`
- Scope / aggregation: `document` / `count`
- Severity / confidence: `low` / `medium`
- False-positive risk: `high`
- Tóm tắt: Nhiều bullet mở bằng nhãn in đậm và dấu hai chấm dù nội dung có thể viết thành câu hoặc bảng.
- Rewrite strategy:
  - Giữ nhãn khi người đọc cần quét; nếu không, viết bullet trực tiếp hoặc dùng bảng.
- Exceptions:
  - Glossary, danh sách thuộc tính, changelog hoặc nội dung cần quét nhanh theo nhãn.

## VI-STY-N01: `don-vi-khong-co-khoang-trang`

- Skill: `style-guide-vi`
- Finding type: `preference`
- Scope / aggregation: `token` / `single`
- Severity / confidence: `low` / `medium`
- False-positive risk: `medium`
- Tóm tắt: Số và ký hiệu đơn vị viết liền trong văn bản khi style dự án yêu cầu một khoảng trắng.
- Rewrite strategy:
  - Theo style guide; mặc định thêm một khoảng trắng giữa số và đơn vị trong văn bản.
- Exceptions:
  - Nhãn UI thiếu chỗ, quy ước ngành, code, identifier hoặc style guide yêu cầu viết liền.

## VI-STY-N02: `phan-tram-khong-nhat-quan`

- Skill: `style-guide-vi`
- Finding type: `preference`
- Scope / aggregation: `document` / `consistency`
- Severity / confidence: `low` / `low`
- False-positive risk: `high`
- Tóm tắt: Trộn dạng phần trăm có và không có khoảng trắng trong cùng tài liệu.
- Rewrite strategy:
  - Chọn dạng theo style guide và áp cho văn bản thường, không sửa dữ liệu hoặc code.
- Exceptions:
  - Trích dẫn, dữ liệu nhập, locale khác nhau hoặc style từng sản phẩm có chủ đích.

## VI-STY-N03: `ngay-thang-mo-ho`

- Skill: `style-guide-vi`
- Finding type: `warning`
- Scope / aggregation: `token` / `single`
- Severity / confidence: `medium` / `medium`
- False-positive risk: `medium`
- Tóm tắt: Ngày viết dạng số ngắn có thể bị hiểu theo thứ tự ngày-tháng hoặc tháng-ngày.
- Rewrite strategy:
  - Dùng tên tháng, ISO 8601 hoặc nêu locale theo style guide.
- Exceptions:
  - Tài liệu nội bộ có locale đã công bố, dữ liệu máy hoặc biểu mẫu bắt buộc.

## VI-STY-P01: `xung-ho-khong-nhat-quan`

- Skill: `style-guide-vi`
- Finding type: `warning`
- Scope / aggregation: `document` / `consistency`
- Severity / confidence: `medium` / `medium`
- False-positive risk: `high`
- Tóm tắt: Trộn nhiều cách gọi độc giả hoặc người viết mà chưa có lý do chức năng.
- Rewrite strategy:
  - Xác định quan hệ với độc giả rồi lập bảng cách gọi; giữ thuật ngữ phân tích khi nó có chức năng riêng.
- Exceptions:
  - Khi "người dùng" là đối tượng phân tích còn "bạn" là lời gọi trực tiếp, hoặc trích dẫn nhiều người nói.

## VI-STY-P02: `chung-ta-ep-dong-thuan`

- Skill: `style-guide-vi`
- Finding type: `warning`
- Scope / aggregation: `sentence` / `single`
- Severity / confidence: `low` / `medium`
- False-positive risk: `medium`
- Tóm tắt: Dùng "chúng ta đều" để trình bày một nhận định như thể người đọc đã đồng ý.
- Rewrite strategy:
  - Nêu nhận định và căn cứ trực tiếp; chỉ dùng "chúng ta" khi nhóm bao gồm người đọc thật sự rõ.
- Exceptions:
  - Lời nói trong nhóm đã có đồng thuận hoặc hoạt động hướng dẫn thật sự cùng làm.

## VI-STY-T01: `login-dang-nhap-lan-lon`

- Skill: `style-guide-vi`
- Finding type: `warning`
- Scope / aggregation: `document` / `consistency`
- Severity / confidence: `low` / `medium`
- False-positive risk: `high`
- Tóm tắt: Trộn "login", "log in" và "đăng nhập" cho cùng một thao tác trong nội dung người dùng.
- Rewrite strategy:
  - Theo glossary hoặc nhãn UI; không đổi tên API, command hay identifier.
- Exceptions:
  - Khi phân biệt nhãn UI, endpoint, sự kiện analytics hoặc trích dẫn nguyên văn.

## VI-STY-T02: `viet-tat-chua-giai-thich`

- Skill: `style-guide-vi`
- Finding type: `warning`
- Scope / aggregation: `document` / `single`
- Severity / confidence: `low` / `low`
- False-positive risk: `high`
- Tóm tắt: Từ viết tắt in hoa xuất hiện trong nội dung phổ thông mà có thể chưa được giải thích.
- Rewrite strategy:
  - Giải thích ở lần đầu theo glossary; bỏ qua tên sản phẩm, đơn vị và từ viết tắt phổ biến với độc giả.
- Exceptions:
  - Từ viết tắt quen thuộc với độc giả, tên sản phẩm, đơn vị, code, bảng glossary hoặc nội dung chuyên gia.

## VI-TRA-L01: `mo-khoa-tiem-nang`

- Skill: `translationese-cleaner-vi`
- Finding type: `warning`
- Scope / aggregation: `phrase` / `single`
- Severity / confidence: `medium` / `high`
- False-positive risk: `low`
- Tóm tắt: Dịch sát "unlock potential" thành "mở khóa tiềm năng" khi ý thực là cho phép hoặc cải thiện một khả năng cụ thể.
- Rewrite strategy:
  - Nêu khả năng, đối tượng và tác động cụ thể đã có trong bản gốc.
- Exceptions:
  - Slogan đã duyệt hoặc ngữ cảnh cố ý dùng ẩn dụ về khóa.

## VI-TRA-L02: `dieu-huong-su-phuc-tap`

- Skill: `translationese-cleaner-vi`
- Finding type: `warning`
- Scope / aggregation: `phrase` / `single`
- Severity / confidence: `medium` / `high`
- False-positive risk: `low`
- Tóm tắt: Dịch "navigate complexity" thành "điều hướng sự phức tạp" thay vì nêu công việc cần xử lý.
- Rewrite strategy:
  - Thay bằng xử lý, theo dõi, lựa chọn hoặc đáp ứng tùy hành động gốc.
- Exceptions:
  - Văn cảnh nói thật về điều hướng trong không gian hoặc giao diện.

## VI-TRA-L03: `tac-dong-co-y-nghia`

- Skill: `translationese-cleaner-vi`
- Finding type: `warning`
- Scope / aggregation: `phrase` / `single`
- Severity / confidence: `medium` / `high`
- False-positive risk: `low`
- Tóm tắt: Dịch "meaningful impact" thành "tác động có ý nghĩa" mà không nêu tác động cụ thể.
- Rewrite strategy:
  - Nêu thay đổi có thể quan sát hoặc giữ mức khái quát nếu bản gốc không có thêm dữ kiện.
- Exceptions:
  - Khi đây là thuật ngữ được định nghĩa bằng tiêu chí ở phần trước.

## VI-TRA-L04: `o-cap-do-cot-loi`

- Skill: `translationese-cleaner-vi`
- Finding type: `preference`
- Scope / aggregation: `phrase` / `single`
- Severity / confidence: `low` / `high`
- False-positive risk: `low`
- Tóm tắt: Dịch "at its core" thành "ở cấp độ cốt lõi" như một lời dẫn tạo vẻ sâu sắc.
- Rewrite strategy:
  - Bỏ lời dẫn hoặc nêu thành phần nền tảng bằng danh từ cụ thể.
- Exceptions:
  - Phân tích kiến trúc có nhiều lớp và "lõi" là một thành phần đã định nghĩa.

## VI-TRA-L05: `tan-dung-moi-ngu-canh`

- Skill: `translationese-cleaner-vi`
- Finding type: `preference`
- Scope / aggregation: `phrase` / `count`
- Severity / confidence: `low` / `medium`
- False-positive risk: `medium`
- Tóm tắt: Dùng "tận dụng" cho mọi trường hợp của "leverage" dù động từ cụ thể tự nhiên hơn.
- Rewrite strategy:
  - Chọn dùng, phân tích, kết hợp, dựa vào hoặc khai thác theo quan hệ thực tế.
- Exceptions:
  - Khi nghĩa thực là khai thác lợi thế hoặc nguồn lực sẵn có.

## VI-TRA-L06: `trai-nghiem-lien-mach`

- Skill: `translationese-cleaner-vi`
- Finding type: `warning`
- Scope / aggregation: `phrase` / `single`
- Severity / confidence: `low` / `medium`
- False-positive risk: `medium`
- Tóm tắt: Dịch "seamless experience" thành "trải nghiệm liền mạch" mà không chỉ ra sự gián đoạn được loại bỏ.
- Rewrite strategy:
  - Mô tả bước chuyển, thời gian chờ hoặc thao tác được bỏ nếu đầu vào có dữ kiện.
- Exceptions:
  - Khi "liền mạch" là thuật ngữ UX đã có tiêu chí hoặc bằng chứng ở phần trước.

## VI-TRA-S01: `thong-qua-viec-day-dac`

- Skill: `translationese-cleaner-vi`
- Finding type: `preference`
- Scope / aggregation: `phrase` / `count`
- Severity / confidence: `medium` / `medium`
- False-positive risk: `medium`
- Tóm tắt: Lặp "thông qua việc" để dịch cấu trúc "by + V-ing" thay vì dùng động từ trực tiếp.
- Rewrite strategy:
  - Đưa hành động sau "việc" thành động từ chính hoặc mệnh đề chỉ cách thức.
- Exceptions:
  - Khi cần nhấn mạnh cơ chế và cấu trúc không bị lặp trong đoạn.

## VI-TRA-S02: `thuc-hien-viec`

- Skill: `translationese-cleaner-vi`
- Finding type: `warning`
- Scope / aggregation: `phrase` / `single`
- Severity / confidence: `medium` / `high`
- False-positive risk: `low`
- Tóm tắt: Dùng động từ nhẹ "thực hiện việc" hoặc "tiến hành thực hiện" trước một hành động rõ.
- Rewrite strategy:
  - Biến danh từ chỉ hành động thành động từ chính, giữ chủ thể và thời gian.
- Exceptions:
  - Khi "việc" là một đối tượng pháp lý đã được định nghĩa và cần tham chiếu nhất quán.

## VI-TRA-S03: `bi-dong-che-tac-nhan`

- Skill: `translationese-cleaner-vi`
- Finding type: `preference`
- Scope / aggregation: `sentence` / `count`
- Severity / confidence: `medium` / `low`
- False-positive risk: `high`
- Tóm tắt: Dùng "được ... bởi" theo tiếng Anh khi tác nhân đã rõ và cần chịu trách nhiệm.
- Rewrite strategy:
  - Đưa tác nhân lên làm chủ ngữ nếu trách nhiệm hoặc hành động là thông tin chính.
- Exceptions:
  - Khi tác nhân không biết, không quan trọng, cần giấu hợp lý hoặc phương pháp khoa học ưu tiên đối tượng.

## VI-TRA-S04: `dua-ra-su-ho-tro`

- Skill: `translationese-cleaner-vi`
- Finding type: `warning`
- Scope / aggregation: `phrase` / `single`
- Severity / confidence: `medium` / `high`
- False-positive risk: `low`
- Tóm tắt: Dùng "đưa ra/cung cấp sự hỗ trợ" thay cho động từ "hỗ trợ" trong câu thông thường.
- Rewrite strategy:
  - Dùng "hỗ trợ" làm động từ và giữ rõ người hỗ trợ, đối tượng, phạm vi.
- Exceptions:
  - Khi "gói hỗ trợ" hoặc "sự hỗ trợ" là danh mục, quyền lợi hay đối tượng đang được phân tích.

Tổng cộng: **40 pattern**.
