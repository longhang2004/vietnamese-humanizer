# Nhóm văn phong để khảo sát tiếp

Khảo sát ngày 3 tháng 11 năm 2026. Đây là danh mục tác vụ đề xuất của dự án, không phải hệ phân loại ngôn ngữ học chuẩn hoặc danh sách preset đã có trong API. Từ v0.6.0, API nhận profile `preserve`, `plain`, `business`, `technical`, `administrative`, `social`, `marketing`. Ba profile mới có [nguồn đọc riêng](research/2026-11-04-administrative-social-marketing.md).

## Phân biệt các lựa chọn

- **Chủ đề/lĩnh vực:** công nghệ, giải trí, du lịch, sức khỏe. Một bài về giải trí có thể là bản tin nghiêm túc hoặc bài bình luận.
- **Thể loại/mục đích:** bản tin, hướng dẫn, review, quảng bá, kể chuyện, giao việc.
- **Kênh:** email, chat, bài dài, caption, lời dẫn để nghe. “Văn nói” còn gồm hội thoại tự phát và bản chép lời; một kịch bản soạn sẵn chưa đại diện cho chúng.
- **Giọng:** thân thiện, trang trọng, vui vẻ, dí dỏm, nghiêm túc, đồng cảm. Một bài marketing không bắt buộc phải hài hước; lời nói trang trọng vẫn là văn nói.
- **Quan hệ và độc giả:** quyết định xưng hô, kiến thức tiền đề và mức trực tiếp phù hợp.

Mô hình nhiều chiều của [NN/g](https://www.nngroup.com/articles/tone-of-voice-dimensions/) và cách điều chỉnh theo tình huống của [Intuit](https://contentdesign.intuit.com/voice-tone/) giúp thiết kế các lựa chọn riêng. Chúng không xác nhận một hệ phân loại hay mức chất lượng cho tiếng Việt.

## Nhóm tác vụ thực dụng

| Nhóm | Cần khảo sát ở bài thật | Điểm dễ sửa sai | Trạng thái đề xuất |
| --- | --- | --- | --- |
| Văn viết rõ ràng | Mạch đoạn, chủ thể, chi tiết và nhịp theo ý | Làm mất nét riêng khi rút gọn | Đã có profile; cần review bản ngữ |
| Công việc | Đề nghị, tiến độ, trách nhiệm và thời hạn | Biến dự kiến thành cam kết | Đã có profile; cần review bản ngữ |
| Kỹ thuật | Tiền đề, thao tác, tham chiếu, thuật ngữ | Đổi code, bỏ điều kiện hoặc thêm bước | Đã có profile; cần review theo ngành |
| Giao tiếp, chăm sóc khách hàng | Trả đúng lượt, xác nhận điều đã biết, câu hỏi tiếp theo | Tự nhận lỗi, hứa xử lý hoặc đổi vai xưng hô | Ưu tiên phát triển hướng dẫn hội thoại đã có |
| Marketing, quảng bá | Lợi ích có căn cứ, thông điệp, lời mời hành động | Bịa công dụng, số liệu, khan hiếm hay lời chứng thực | Đã có profile từ v0.6.0; cần review bản ngữ |
| Social, caption, lời mời | Mở đầu đúng nhu cầu, thông tin cốt lõi, bước tiếp theo | Giật tít, thêm emoji hoặc ép mọi bài thật ngắn | Đã có profile từ v0.6.0; cần review bản ngữ |
| Kịch bản nói, video, podcast | Nhịp nghe, chuyển ý, cách đọc số và tham chiếu hình ảnh | Chép nguyên cấu trúc bài dài hoặc thêm ngập ngừng giả | Ưu tiên mở rộng hướng dẫn đã có |
| Giải thích, giáo dục | Kiến thức tiền đề, ví dụ, quan hệ khái niệm | Ví dụ sai, giảng giải quá mức hoặc đơn giản hóa sai | Khảo sát cùng tài liệu kỹ thuật |
| Báo chí, bản tin, thông báo | Thông tin chính, quy nguồn, sự kiện và nhận định | Đưa bình luận thành sự thật hoặc thêm địa điểm | Có pilot nhỏ; cần nhiều nguồn khác nhau |
| Kể chuyện, blog cá nhân, tản văn | Điểm nhìn, trình tự, chi tiết, nhịp và cảm xúc | Bịa trải nghiệm hoặc biến mọi đoạn thành giọng trữ tình | Khảo sát bằng tư liệu có quyền rõ |
| Review, phê bình | Căn cứ đánh giá, tiêu chí, trải nghiệm và giới hạn | Giả vờ đã dùng/xem, ép nhận xét tích cực | Thử sau khi có rubric riêng |
| Bình luận, lập luận | Luận điểm, bằng chứng, phản biện và mức chắc chắn | Tăng mức khẳng định hoặc xóa phản biện | Cần kiểm bảo toàn lập trường riêng |
| Hành chính | Thể loại văn bản, mẫu duyệt, thẩm quyền và trách nhiệm | Câu đúng văn phong nhưng sai mẫu hoặc nghĩa vụ | Đã có profile từ v0.6.0; cần reviewer lĩnh vực |
| Học thuật | Thuật ngữ, phương pháp, hạn chế và dẫn nguồn | Xóa dè dặt khoa học hoặc bịa citation | Cần nguồn và reviewer theo chuyên ngành |

Các hàng là nhóm tác vụ, có chỗ giao nhau. Chưa thêm đồng loạt vào enum `profile`: trước hết cần bài đọc đa tác giả, cặp cần sửa/giữ nguyên và một đợt đánh giá cho từng nhóm.

## Vui vẻ, đùa giỡn và hài hước

Nên thử như các lựa chọn giọng có mức độ, kết hợp với tác vụ và quan hệ:

- **Vui vẻ:** nhịp sáng, lời mời tích cực; có thể hoàn toàn không có câu đùa.
- **Dí dỏm nhẹ:** một liên tưởng hoặc cách nói bất ngờ vẫn giữ rõ thông tin. Pilot đổi sách có thử một cách nhân hóa do agent tự viết.
- **Đùa thân mật:** cần quan hệ và giới hạn người dùng xác định; không mặc định thân mật với khách lạ.
- **Châm biếm/giễu nhại:** cần xác định đối tượng, chủ đích và phạm vi sáng tạo; chưa có hướng dẫn đủ để làm preset.

Tiêu chí là câu đùa hợp tình huống và người đọc có thấy nó có duyên không. Chèn “nha”, emoji hoặc dấu chấm than không đủ tạo giọng tự nhiên. Lời báo lỗi, thông tin chậm trễ và tình huống người đọc đang lo cần cách xử lý riêng. [Atlassian](https://atlassian.design/foundations/content/voice-tone/) phân biệt những điểm nhấn tạo cảm giác dễ chịu với việc cố gây cười và nhấn mạnh thời điểm sử dụng.

## Nguồn đã đọc và phạm vi vận dụng

Chỉ lưu metadata và nhận xét bằng lời riêng. Các bài là nguồn có tác giả/đơn vị biên tập được công bố; chưa xác minh lịch sử sản xuất từng câu. Thời điểm xuất bản cũ là dấu hiệu xuất xứ hữu ích, không thay thế việc xác minh bản lưu.

| Nguồn | Xuất xứ | Quan sát của dự án và giới hạn |
| --- | --- | --- |
| [Hội sách Xuân 2018](https://baochinhphu.vn/hoi-sach-xuan-2018-hoi-sach-cu-lon-nhat-nam-102235514.htm) | Nhật Nam, Báo Điện tử Chính phủ, 06-03-2018 | Phần đầu nêu sự kiện, thời gian, địa điểm; phần sau thêm chất liệu gợi hình. Không coi mọi từ quảng bá trong bài là cần sao theo. Dùng làm mẫu đọc cùng chủ đề sách, không dùng dữ kiện sự kiện này cho pilot giả định. |
| [Bài về thói quen đọc sách](https://tuoitre.vn/nha-van-nguyen-nhat-anh-toi-me-doc-sach-tu-chuyen-ke-cua-ba-20190420081641818.htm) | Nguyễn Nhật Ánh, Tuổi Trẻ, 20-04-2019 | Quan sát nhịp kể xen suy ngẫm và vai trò của chi tiết cá nhân. Dự án chỉ tham khảo cách tổ chức; không lấy ký ức của tác giả làm trải nghiệm của writer. |
| [Ông hỏi tui tui biết hỏi ai](https://tuoitre.vn/ong-hoi-tui-tui-biet-hoi-ai-20180711112812921.htm) | Bút Bi, Tuổi Trẻ, 11-07-2018 | Tiểu phẩm dùng lượt hỏi–đáp ngắn, khẩu ngữ và nhân hóa để tạo ý châm biếm. Đây là hội thoại sáng tác đã biên tập, không phải bản ghi lời nói tự phát. Đọc sau khi chốt bản sửa pilot, chỉ dùng để đặt hướng nghiên cứu tiếp; không sao vai xưng hô hoặc chi tiết của bài sang tình huống khác. |
| [Case study Biti’s Hunter](https://www.buzzmetrics.com/bai-viet-bsi/bsi-case-study-bitis-hunter-chien-dich-di-de-tro-ve-2) | Buzzmetrics; bài nêu Kim Đỗ trao đổi với Phú Cường; trang hiển thị 21-03-2018 và 17-10-2024 | Có bối cảnh, đối tượng và thông điệp thương hiệu. Chưa xác minh ý nghĩa của hai mốc ngày hoặc lịch sử sửa trang. Không dùng số liệu chiến dịch để kết luận cách viết nào tốt hơn. |
| [Educational content](https://styleguide.mailchimp.com/writing-educational-content/) | Mailchimp Content Style Guide | Tham khảo cách xác định mục tiêu và kiến thức nền của người học. Không chuyển giới hạn độ dài câu tiếng Anh thành luật tiếng Việt. |
| [Social media](https://styleguide.mailchimp.com/writing-for-social-media/) | Mailchimp Content Style Guide | Tham khảo sự tập trung và phù hợp tình huống. Không dùng các tên nền tảng/giới hạn ký tự trên trang làm thông số hiện hành cho sản phẩm. |
| [Email newsletters](https://styleguide.mailchimp.com/writing-email-newsletters/) | Mailchimp Content Style Guide | Tham khảo phân cấp nội dung và làm rõ bước tiếp theo. Không bắt mọi email giao dịch có cấu trúc marketing. |
| [Voice and tone](https://contentdesign.intuit.com/voice-tone/) | Intuit Content Design | Tham khảo việc tách giọng thương hiệu và sắc thái theo ngữ cảnh. Không lấy một thương hiệu làm chuẩn cho mọi người viết. |
| [Voice and tone](https://atlassian.design/foundations/content/voice-tone/) | Atlassian Design | Tham khảo khác biệt giữa thông báo chức năng và điểm nhấn vui phù hợp. Không suy ra đây là bằng chứng người đọc Việt thích một câu đùa. |
| [Tone dimensions](https://www.nngroup.com/articles/tone-of-voice-dimensions/) | Kate Moran, NN/g, 17-07-2016; trang nêu review 16-08-2023 | Tham khảo cách biểu diễn nhiều chiều và đánh giá cảm nhận người đọc. Nghiên cứu không đánh giá các profile của repo. |

Chưa có tập nguồn tiếng Việt đủ rộng cho mọi hàng trong bảng. Giải trí, lời nói tự phát, đùa thân mật, hành chính và học thuật cần các đợt thu thập riêng; không suy rộng từ hai bài về sách hoặc một tiểu phẩm. Quy tắc chuyển quan sát thành hướng dẫn nằm trong [learning loop](style-learning-loop.md).
