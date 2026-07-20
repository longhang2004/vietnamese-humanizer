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
- Good examples:
  - `clean_rewrite`: Các tài liệu này cần được lưu lại.
  - `clean_rewrite`: Những nhân viên trên đều đã xử lý yêu cầu.
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
- Good examples:
  - `clean_rewrite`: Vì trời mưa, trận đấu bị hoãn.
  - `clean_rewrite`: Máy hết pin nên dữ liệu chưa đồng bộ.
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
- Good examples:
  - `clean_rewrite`: Việc máy chủ dừng giữa lúc sao lưu làm nhóm lo ngại.
    - Context: Nhóm xác nhận việc máy chủ dừng là nguyên nhân gây lo ngại.
  - `clean_rewrite`: Tin Mai nghỉ việc khiến quản lý bất ngờ.
    - Context: Lan xác nhận Mai là người đã nghỉ.
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
- Good examples:
  - `clean_rewrite`: Báo cáo mới của nhóm đã được gửi sáng nay.
  - `clean_rewrite`: Hệ thống theo dõi đơn hàng và sẽ gửi cảnh báo khi có lỗi.
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
- Good examples:
  - `clean_rewrite`: Nhóm sẽ gửi kết quả vào chiều nay.
  - `clean_rewrite`: Hệ thống đang khởi động lại.
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
- Good examples:
  - `clean_rewrite`: Bác sĩ chẩn đoán bệnh nhân bị viêm phổi.
  - `clean_rewrite`: Công cụ hỗ trợ chẩn đoán lỗi mạng.
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
- Good examples:
  - `clean_rewrite`: Hai phòng ban sẽ sáp nhập từ tháng 8.
  - `clean_rewrite`: Kế hoạch sáp nhập đã được công bố.
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
- Good examples:
  - `clean_rewrite`: Báo cáo đã xong, vui lòng kiểm tra.
  - `clean_rewrite`: Bạn đã nhận được email chưa?
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
- Good examples:
  - `clean_rewrite`: Bản A đã duyệt, bản B còn chờ.
  - `clean_rewrite`: Lưu ý: không tắt máy.
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
- Good examples:
  - `clean_rewrite`: Vui lòng gửi báo cáo ngay!
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Vì sao hệ thống dừng?
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Cache giữ dữ liệu đã đọc để giảm số lần truy cập nguồn.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Ba nguyên tắc này giúp API thay đổi mà không phá client cũ.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Cấu hình mới có hiệu lực từ lần khởi động tiếp theo.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Nhóm sẽ chốt phương án tại cuộc họp ngày 25 tháng 7.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `review_comment`: Cần bổ sung nguồn cụ thể cho nhận định rằng phương pháp hoàn toàn an toàn.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `review_comment`: Cần xác định các nghiên cứu về tác động của mô hình lên năng suất.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Tính năng này quan trọng đối với việc cải thiện hiệu suất.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Người quản lý có vai trò then chốt đối với việc duy trì tiến độ.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Doanh nghiệp cần đổi mới.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Kỹ năng số rất quan trọng.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `review_comment`: Cần có tiêu chí so sánh trước khi gọi hiệu năng “vượt trội”; thông tin hiện có chỉ xác nhận công cụ xử lý 2.000 bản ghi mỗi phút trong thử nghiệm nội bộ.
    - Reason: Không xóa đánh giá của tác giả hoặc biến dữ kiện thành câu thay thế khi thiếu căn cứ.
  - `review_comment`: Cần có tiêu chí chất lượng trước khi gọi gói này “đẳng cấp”; thông tin hiện có chỉ xác nhận bảo hành 24 tháng và hỗ trợ trong giờ hành chính.
    - Reason: Không tự quyết định bỏ lập trường đánh giá khi chưa có bằng chứng.
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
- Good examples:
  - `clean_rewrite`: Cập nhật giúp giảm lỗi; kiểm thử giúp tăng độ ổn định.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Họp sớm là việc cần thiết; gửi tài liệu trước cũng quan trọng.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Công cụ mở tệp 2 GB trong 4 giây và có phím tắt cho các thao tác chính.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Khóa học có sáu bài thực hành và một buổi phản biện.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Hệ thống lưu log và gửi cảnh báo để giúp nhóm phản hồi, từ đó nâng cao chất lượng.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Nhóm sửa lỗi, cập nhật tài liệu và qua đó tạo ra giá trị.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Nhóm nhận yêu cầu sáng nay, kiểm tra dữ liệu vào buổi trưa và sẽ gửi kết quả cuối ngày. Sau cuộc họp, nhóm lưu biên bản và đóng yêu cầu khi hoàn tất.
  - `clean_rewrite`: Máy chủ ghi log mỗi phút và hệ thống gửi báo cáo mỗi giờ. Nhân viên xem dashboard hằng ngày; bộ phận sao lưu dữ liệu mỗi tuần, còn quản lý rà báo cáo mỗi tháng.
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
- Good examples:
  - `clean_rewrite`: Chúng tôi cung cấp giải pháp cho mọi khách hàng.
  - `clean_rewrite`: Sản phẩm này đi kèm dịch vụ bảo hành.
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
- Good examples:
  - `clean_rewrite`: Trang tải nhanh; dữ liệu được mã hóa.
  - `clean_rewrite`: 1. Nhập email. 2. Nhập mật khẩu.
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
- Good examples:
  - `clean_rewrite`: - Trang tải nhanh. - Dữ liệu được mã hóa.
  - `clean_rewrite`: 1. Mở file. 2. Chọn Lưu.
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
- Good examples:
  - `clean_rewrite`: Tệp có dung lượng 5 GB.
  - `clean_rewrite`: Mẫu được giữ ở 4 °C.
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
- Good examples:
  - `clean_rewrite`: Tỷ lệ A là 15%, còn tỷ lệ B là 20%.
  - `clean_rewrite`: Chiết khấu 5% được dùng ở cả bảng và phần mô tả.
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
- Good examples:
  - `clean_rewrite`: Hạn chót là ngày 7 tháng 8 năm 2026.
    - Context: Tài liệu dùng thứ tự ngày/tháng/năm.
  - `needs_author_decision`: Cần xác nhận “26” thuộc thế kỷ nào trước khi đổi định dạng ngày.
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
- Good examples:
  - `clean_rewrite`: Bạn chọn gói rồi xác nhận địa chỉ.
    - Context: Style guide quy định gọi độc giả là “bạn”.
  - `needs_author_decision`: Cần xác nhận “chúng ta” có bao gồm người đọc hay chỉ phía “chúng tôi” trước khi sửa câu.
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
- Good examples:
  - `clean_rewrite`: AI sẽ thay đổi mọi ngành.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Quy trình này rất đơn giản.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Chọn Đăng nhập, sau đó đăng nhập bằng email.
    - Context: Style guide quy định nhãn UI là “Đăng nhập”.
  - `clean_rewrite`: Nếu đăng nhập lỗi, hãy mở lại trang Đăng nhập.
    - Context: Style guide quy định dùng “đăng nhập” trong nội dung người dùng.
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
- Good examples:
  - `clean_rewrite`: Thỏa thuận mức dịch vụ (SLA) sẽ được rà trong cuộc họp.
    - Context: Glossary định nghĩa SLA là “thỏa thuận mức dịch vụ”.
  - `clean_rewrite`: Mục tiêu thời gian khôi phục (RTO) được dùng để quyết định phương án khôi phục.
    - Context: Glossary định nghĩa RTO là “mục tiêu thời gian khôi phục”.
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
- Good examples:
  - `clean_rewrite`: Công cụ giúp tìm xu hướng trong dữ liệu bán hàng.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Khóa học phát triển năng lực lãnh đạo qua bài tập giao việc và phản hồi.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Nền tảng giúp doanh nghiệp theo dõi các yêu cầu tuân thủ.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Hướng dẫn giải thích cách khai và nộp thuế hộ kinh doanh.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Chương trình hỗ trợ thiết thực bằng cách cấp học bổng cho 35 học sinh trong năm 2025.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Mỗi 200.000 đồng đóng góp tạo hỗ trợ thiết thực bằng cách chi trả một bộ sách.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Sản phẩm này là một nền tảng dữ liệu.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Vấn đề chính nằm ở cách hai nhóm trao đổi yêu cầu.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Nhóm dùng AI để viết báo cáo.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Ứng dụng dùng nền tảng để gửi thông báo.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Việc chỉ đăng nhập một lần trên web và di động giúp trải nghiệm không bị gián đoạn.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Bản nháp được giữ khi người dùng đổi thiết bị, nên quá trình làm việc không bị gián đoạn.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Hệ thống tự kiểm tra dữ liệu để giảm lỗi.
  - `clean_rewrite`: Nhóm dùng mẫu có sẵn để tiết kiệm thời gian.
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
- Good examples:
  - `clean_rewrite`: Nhóm đánh giá hồ sơ vào thứ Hai.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Kỹ thuật viên kiểm tra máy.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
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
- Good examples:
  - `clean_rewrite`: Giám đốc phê duyệt báo cáo vào sáng nay.
  - `clean_rewrite`: Nhóm vận hành phát hiện lỗi trong ca đêm.
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
- Good examples:
  - `clean_rewrite`: Nhóm sẽ hỗ trợ khách hàng mới.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
  - `clean_rewrite`: Bộ phận IT hỗ trợ trong giờ làm việc.
    - Reason: Giữ các dữ kiện đã có và chỉ sửa cấu trúc mục tiêu.
- Exceptions:
  - Khi "gói hỗ trợ" hoặc "sự hỗ trợ" là danh mục, quyền lợi hay đối tượng đang được phân tích.

Tổng cộng: **40 pattern**.
