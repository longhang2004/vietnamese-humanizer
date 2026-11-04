# Ghi chú nghiên cứu

Truy cập nguồn ngày 20 tháng 7 năm 2026. Repository không nhập dataset hay sao chép nội dung từ các nguồn dưới đây.

## Đợt đọc về văn phong ngày 31 tháng 10 năm 2026

Xem [nguồn có tác giả và ghi chú vận dụng](../skills/humanizer-vi/references/sources.md): phỏng vấn Nguyễn Ngọc Tư do Hoàng Thu Phố thực hiện trên Nhân Dân/Thời Nay, bài Nam Kha ghi nhận chia sẻ của Nguyễn Khắc Cường trên Mực Tím/Tuổi Trẻ, và nghiên cứu về profile giao tiếp tiếng Việt. Ghi chú tách điều quan sát được, quyết định của dự án và giới hạn bằng chứng. Không đưa nguyên văn bài báo vào corpus hay prompt.

Đợt này bổ sung hướng dẫn mạch đoạn, kết hợp từ, lược chủ ngữ, phép lặp, sắc thái và cách biên tập theo kênh. Ba mươi benchmark dài mới do coding agent tự viết theo 15 cặp đối chiếu; không phải văn bản người thật hoặc dữ liệu được các tác giả nguồn duyệt. Các cặp được xem là cùng một nhóm khi chia development/test để tránh rò nội dung.

## Đợt khảo sát cùng chủ đề ngày 3 tháng 11 năm 2026

[Learning loop](style-learning-loop.md) mô tả cách đọc nhiều nguồn có tác giả, tạo brief riêng, cho writer viết độc lập, biên tập và kiểm trên chủ đề chưa thấy. [Style catalog](style-catalog.md) tách chủ đề, thể loại, kênh, giọng và quan hệ; ghi nguồn mới về bản tin, kể chuyện, marketing, social, giáo dục và UX.

[Pilot đổi sách](research/2026-11-03-same-topic-pilot.md) đã chạy một writer subagent, agent chính biên tập và một reviewer subagent với bản A/B ẩn nhãn. Dữ kiện giả định, output AI và nhận xét AI được lưu riêng khỏi corpus/benchmark. Đây là quan sát development, không phải baseline bản ngữ hoặc bằng chứng định lượng về cải thiện.

## Khảo sát lối viết theo khuôn ngày 4 tháng 11 năm 2026

Xem [nhật ký nguồn](research/2026-11-04-formulaic-prose.md): báo cáo Graphite cập nhật đến 21-10-2026, Pew, bài biên tập của Steph Zinn, newsletter Base và các thảo luận Reddit. Bài X được dẫn lại nhưng truy cập trực tiếp trả 403; chưa dùng nội dung chưa kiểm chứng làm căn cứ chính. Các nguồn chủ yếu bằng tiếng Anh.

Đợt này thêm reference xét đối lập, lời tự nhấn ý, kết đoạn lặp, bố cục chia nhỏ và giọng trợ lý theo chức năng. Thêm 12 case tiếng Việt tự viết có đối chiếu cần sửa/cần giữ; không thêm regex hoặc dùng giảm số dấu hiệu làm điểm chất lượng.

Đợt [bổ sung nguồn Việt](research/2026-11-04-vietnamese-writing-discussions.md) đọc Phạm Mỹ, Upcontent, Hoà Lương, VOZ, Tinh tế và Finhay. Bổ sung việc rà khuôn lời chúc/tri ân, thông tin riêng của đối tượng và chức năng dấu câu; ghi rõ tuổi nguồn, phần chỉ là trải nghiệm và lời khuyên không được vận dụng.

## Agent Skills

[Agent Skills specification](https://agentskills.io/specification) quy định skill là một thư mục có `SKILL.md`. Frontmatter bắt buộc `name` và `description`; tên dùng chữ thường, số, dấu gạch nối và phải trùng tên thư mục. Specification khuyến nghị `SKILL.md` dưới 500 dòng, reference tương đối và progressive disclosure. Repository specification dùng Apache-2.0 cho code và CC-BY-4.0 cho tài liệu. Dự án này chỉ áp dụng format và tự viết nội dung.

## Dự án humanizer

- [blader/humanizer](https://github.com/blader/humanizer) dùng MIT License. Dự án học workflow nhận diện pattern, viết lại, audit và bảo toàn giọng. Phần không chuyển nguyên sang tiếng Việt gồm `-ing`, title case và một số dấu câu đặc thù tiếng Anh.
- [Humanizer-zh](https://github.com/op7418/Humanizer-zh) dùng MIT License và chủ yếu chuyển thể taxonomy tiếng Anh. Nguồn này cho thấy bản địa hóa cần nêu attribution, nhưng dịch taxonomy chưa đủ cho tiếng Việt.
- [DaleSeo/korean-skills](https://github.com/DaleSeo/korean-skills) tách humanizer và style guide theo đặc điểm tiếng Hàn. Dự án hiện tại xem spacing, register và translationese là các lớp riêng, không sao chép pattern tiếng Hàn.
- Một số dự án thương mại và community định vị bằng bypass detector. Cách định vị này nằm ngoài phạm vi vì detector không đo chất lượng viết và khuyến khích sửa sai mục tiêu.

## Nghiên cứu và dataset tiếng Việt

- [ViSP, Findings of NAACL 2025](https://aclanthology.org/2025.findings-naacl.59/) công bố 1,2 triệu cặp paraphrase từ nhiều domain, được xây bằng kết hợp sinh tự động và đánh giá thủ công. Bài báo nêu rằng paraphrase có nhiều dạng hợp lệ; dự án vì thế dùng rubric thay đáp án vàng duy nhất. Dataset được công bố cho mục đích nghiên cứu; cần kiểm license cụ thể trước khi nhập dữ liệu.
- [ViDetect](https://arxiv.org/abs/2405.03206) gồm 6.800 bài luận, cân bằng giữa văn bản người viết và LLM. Dữ liệu chỉ tập trung essay và nhãn nguồn gốc. Vì vậy, nó không đại diện cho email, tài liệu kỹ thuật hay chất lượng biên tập. Dự án không dùng ViDetect để huấn luyện rule và không tạo detector.
- [VnCoreNLP](https://aclanthology.org/N18-5012/) cung cấp các thành phần NLP tiếng Việt như word segmentation và dependency parsing. MVP chưa thêm model này để giữ dependency nhẹ. Đây là hướng nghiên cứu cho kiểm tra cấu trúc trong phiên bản sau.
- [EVBCorpus](https://aclanthology.org/W13-4301/) là corpus song ngữ Anh-Việt nhiều lớp cho nghiên cứu ngôn ngữ so sánh. Nó có thể dùng để thiết kế nghiên cứu translationese, nhưng repository chưa nhập câu vì cần rà quyền sử dụng và quy trình gán nhãn riêng.
- [Good Spelling of Vietnamese Texts](https://aclanthology.org/P00-1076/) cho thấy sửa chính tả tiếng Việt cần ngữ cảnh và xử lý từ ghép, không chỉ so từ với từ điển. MVP chỉ giữ một số rule có độ tin cậy cao.

## Giả thuyết taxonomy tiếng Việt

Ví dụ và unit test nội bộ đã có cho khoảng trắng quanh dấu câu, lặp từ liền nhau, một số lỗi chính tả phổ biến, business cliché dịch sát, danh hóa bằng "thực hiện việc", xưng hô không nhất quán và cách trình bày đơn vị.

Các heuristic cần đánh giá thêm gồm độ dài câu đồng đều, mật độ từ nối, danh sách ba ý, dấu phẩy tách chủ vị qua regex, từ viết tắt chưa giải thích, giọng quảng cáo và đại từ ép đồng thuận. Những tín hiệu này không chứng minh lỗi hay nguồn gốc tác giả.

## Rủi ro bias

Văn viết miền Bắc, Trung và Nam có thể khác nhau. Tiểu từ như "nha", "nhé", "ạ" phụ thuộc quan hệ, vùng và thế hệ. Thuật ngữ kỹ thuật có thể trông máy móc nhưng vẫn đúng. Văn bản pháp lý, hành chính và học thuật có convention riêng. Reviewer cần ghi domain và register, tìm phản ví dụ và tránh lấy văn phong của một nhóm làm chuẩn duy nhất.

## Việc cần xác minh sau MVP

- License và khả năng tái sử dụng từng phần của ViSP, ViDetect và EVBCorpus.
- Precision của từng regex trên corpus đa miền có sự đồng ý và ẩn danh phù hợp.
- Mức đồng thuận giữa reviewer ở các vùng và ngành.
- Tác động của word segmentation đến đo độ dài câu, lặp từ và cụm danh từ.
