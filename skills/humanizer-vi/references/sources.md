# Nguồn đọc về văn phong

Đọc ngày 31 tháng 10 năm 2026. Các nguồn dưới đây có tên tác giả hoặc người trả lời được công bố. Đây là cơ sở quy nguồn, không phải chứng nhận cách từng câu được sản xuất. Dự án không sao chép bài báo, nhập chúng làm corpus hay mô phỏng giọng riêng của tác giả. Ví dụ và benchmark mới do coding agent tự viết, chưa được reviewer bản ngữ độc lập duyệt.

## Nguồn cho hành chính, mạng xã hội và marketing

Đọc ngày 04-11-2026. Nhật ký và giới hạn truy cập nằm trong `docs/research/2026-11-04-administrative-social-marketing.md` của repository. Ví dụ trong các reference tương ứng do agent tự viết; chưa có human review.

- Bộ Nội vụ trả lời trên Cổng TTĐT Chính phủ, [Cấp số văn bản hành chính theo quy định nào?](https://chinhsachonline.chinhphu.vn/cap-so-van-ban-hanh-chinh-theo-quy-dinh-nao-77131.htm), 19-01-2025; và [Phần căn cứ ban hành văn bản chữ nghiêng hay thường?](https://baochinhphu.vn/phan-can-cu-ban-hanh-van-ban-chu-nghieng-hay-thuong-102230425132226725.htm), 26-04-2023. Vận dụng: giữ mẫu/loại văn bản, số và ký hiệu; không tự điền phần thuộc quy định riêng của cơ quan. Đây không phải công cụ xác nhận tuân thủ pháp luật.
- Bộ KH&CN, [Lấy ý kiến báo cáo sơ bộ và báo cáo chuyên đề](https://mst.gov.vn/bo-khcn-lay-y-kien-bao-cao-so-bo-va-bao-cao-chuyen-de-ve-tong-ra-soat-he-thong-vbqppl-197260905165716969.htm), 05-09-2026. Đọc phần công văn đăng lại, quan sát người nhận, nhiệm vụ và hạn cụ thể. Không suy ra hệ quả của việc không phản hồi trong các văn bản khác.
- cuhiep, Tinh tế, [Đồ nghề siêu gọn nhẹ đi làm content IFA 2026](https://tinhte.vn/thread/do-nghe-sieu-gon-nhe-di-lam-content-ifa-2026.4175741/), 11-09-2026. Tham khảo giọng cá nhân, quan hệ cộng đồng và bài trải nghiệm dài; không xác nhận nhận định sản phẩm hoặc áp một cách gọi người đọc cho mọi bài.
- Biti’s, [Thông báo voucher](https://bitis.com.vn/blogs/news/bitis-tang-voucher-giam-50k-ky-niem-50-nam-giai-phong-mien-nam), 24-04-2025. Quan sát giọng hào hứng đi cùng đầy đủ điều kiện. Ưu đãi đã hết hạn; chỉ dùng làm mẫu biên tập theo ngữ cảnh.
- Mailchimp, [Writing for Social Media](https://styleguide.mailchimp.com/writing-for-social-media/), không thấy ngày. Tham khảo quan hệ với người đọc và cách cân nhắc lời xin tương tác; không áp số câu gợi ý hay thông số nền tảng cũ thành quy tắc chung.
- Google Ads, [Misrepresentation](https://support.google.com/adspolicy/answer/6020955?hl=en), không thấy ngày. Vận dụng có giới hạn: giữ giá/điều kiện và không tự thêm bằng chứng, lời hứa hoặc ưu đãi. Chính sách của một nền tảng không xác nhận mọi nội dung marketing đã hợp lệ; nguồn này không được coi là mẫu người Việt tự viết.

## Tiếng Việt được người viết sử dụng

- Hoàng Thu Phố thực hiện phỏng vấn Nguyễn Ngọc Tư, [Viết là cách tôi giao lưu với bạn đọc](https://nhandan.vn/viet-la-cach-toi-giao-luu-voi-ban-doc-post348644.html), Nhân Dân/Thời Nay, 31-01-2019. Quan sát của dự án: nhịp câu không đều vẫn theo được vì đối tượng và lập trường xuyên suốt; cách xưng hô và sắc thái cá nhân không cần chuẩn hóa thành giọng doanh nghiệp. Đây là mẫu hội thoại đã biên tập, không đại diện cho mọi văn nói hoặc mọi vùng miền.
- Nam Kha, [Viết sao cho hay, viết gì cho chất?](https://muctim.tuoitre.vn/viet-sao-cho-hay-viet-gi-cho-chat-101230629160346324.htm), Mực Tím/Tuổi Trẻ, 29-06-2023; ghi nhận chia sẻ của nhà báo Nguyễn Khắc Cường. Bài bàn về chất liệu quan sát và việc giữ mạch khi viết. Vận dụng của dự án: ưu tiên chi tiết đã có trong input/context và kiểm tra mạch đoạn. Với tác vụ biên tập, việc bịa thêm chi tiết để làm sinh động vẫn bị cấm.

## Nghiên cứu để thiết kế đánh giá

- Zheng-Yu Huang và Richard Tzong-han Tsai, [Evaluating Pragmatic Appropriateness in English–Vietnamese Machine Translation with Dyadic Profiles](https://aclanthology.org/2026.wmt-main.16/), WMT 2026. Nghiên cứu nhỏ phân biệt câu đúng/tự nhiên với câu hợp quan hệ người gửi–người nhận. Không phát hiện cải thiện tổng thể có ý nghĩa thống kê từ việc thêm profile; một số phép so sánh cho thấy khác biệt phụ thuộc quan hệ. Dự án tham khảo cách đánh giá riêng tính phù hợp quan hệ và so sánh cặp; bộ hiện tại chưa tái lập thử nghiệm đảo vai và không coi profile là bảo đảm chất lượng.
- Sang Quang Nguyen và Kiet Van Nguyen, [A Large-Scale Benchmark for Vietnamese Sentence Paraphrases](https://aclanthology.org/2025.findings-naacl.59/), Findings of NAACL 2025. ViSP là nghiên cứu paraphrase ở cấp câu với sinh tự động và đánh giá thủ công. Dự án tham khảo việc đánh giá nhiều cách diễn đạt; không nhập dataset hoặc xem điểm tương đồng là bằng chứng giữ nguyên mọi sắc thái.

## Nguồn bổ sung cho writing profiles

Đọc ngày 3 tháng 11 năm 2026. Các nguồn dưới đây được xuất bản bởi tác giả hoặc đội ngũ biên tập được nêu rõ. Việc quy nguồn không chứng nhận từng câu là do con người viết; không sao chép các trang thành corpus.

- Google for Developers, [Voice and tone](https://developers.google.com/style/tone): hướng dẫn giọng gần gũi, rõ và tôn trọng người đọc trong tài liệu developer. Vận dụng: profile kỹ thuật cho phép giọng thân thiện và ưu tiên thông tin hữu ích. Không áp trực tiếp quy tắc ngôi thứ hai, tiếng lóng hay dấu câu tiếng Anh thành luật tiếng Việt.
- Google for Developers, [Procedures](https://developers.google.com/style/procedures): phân biệt tổ chức thao tác theo trình tự và cách trình bày hành động. Vận dụng: giữ quan hệ phụ thuộc, điều kiện và kết quả đã biết. Dự án bổ sung quy tắc không bịa bước, code hoặc đường dẫn vì tác vụ ở đây là biên tập đầu vào.
- Mailchimp, [Voice and tone](https://styleguide.mailchimp.com/voice-and-tone/): phân biệt giọng nhất quán với sắc thái thay đổi theo tình huống, ưu tiên rõ ràng và tránh cố gây cười. Vận dụng: tách profile khỏi register/channel, giữ lời xin lỗi có dụng ý, không tự thêm câu đùa vào cập nhật sự cố. Không lấy giọng thương hiệu Mailchimp làm mặc định tiếng Việt.
- Kate Moran, Nielsen Norman Group, [The Four Dimensions of Tone of Voice](https://www.nngroup.com/articles/tone-of-voice-dimensions/): phân tích giọng theo nhiều chiều và kiểm tra cảm nhận của người đọc. Vận dụng: đánh giá register fit riêng với preservation và cho reviewer xét cùng nội dung trong nhiều tình huống. Nghiên cứu này không xác nhận chất lượng của ba profile tiếng Việt.
- Nhóm ZaloPay Open Source (`phamtai97`, `thinhdang`, `quocanh1897`, `thoainguyen`, `anhldbk`), [Go Language Advanced Programming — Giới thiệu](https://zalopay-oss.github.io/go-advanced/): tài liệu kỹ thuật tiếng Việt nêu rõ độc giả đã biết Go cơ bản và phạm vi chủ đề nâng cao. Quan sát của dự án: cần xác định kiến thức tiền đề trước khi quyết định giải thích thuật ngữ đến đâu. Chỉ đọc phần giới thiệu trong đợt này; không suy ra mọi chương đều cùng phong cách, không sao chép code hoặc nhập sách vào corpus.

Ví dụ trong [plain writing](plain-writing.md), [business writing](business-writing.md), [technical writing](technical-writing.md) và `benchmarks/cases/writing-profiles.jsonl` do coding agent tự viết. Chưa có reviewer bản ngữ độc lập hoặc kết quả đo cải thiện. Nguồn báo chí tiếng Việt ở trên giúp đối chiếu mạch và giọng, chưa đại diện cho tài liệu công việc hay kỹ thuật Việt Nam.

Các nguồn bổ sung chỉ được liên kết và diễn giải ngắn cho mục đích nghiên cứu. Chưa đánh giá quyền tái phân phối toàn văn của từng nguồn; không coi giấy phép MIT của dự án là giấy phép cho nội dung bên ngoài.

## Nguồn bổ sung về lối viết theo khuôn

Đọc ngày 04-11-2026. Phần vận dụng nằm trong [sửa lối viết theo khuôn](formulaic-prose.md); nhật ký đầy đủ ở `docs/research/2026-11-04-formulaic-prose.md` của repository. Chỉ tổng hợp bằng lời riêng, không nhập bài nguồn làm corpus.

- Druck, Paredes và Smith, Graphite — [nghiên cứu gốc, 16-09-2026](https://graphite.io/research/ai-tells), cập nhật [01-10](https://graphite.io/research/ai-tells-opus-5-5-update) và [21-10-2026](https://graphite.io/research/ai-tells-gemini-4-argon-update). Tham khảo các nhóm cấu trúc và sự thay đổi theo model; cùng một họ nghiên cứu bài web, chưa kiểm chứng cho tiếng Việt. Điểm văn hoa có model chấm.
- Bestvater và cộng sự, Pew Research Center — [How Much of the Internet Is Written With AI?](https://www.pewresearch.org/data-labs/2026/08/20/how-much-of-the-internet-is-written-with-ai/), 20-08-2026. Tham khảo giới hạn suy luận từ xu hướng trong tập lớn sang từng bài. Không dùng detector của nghiên cứu làm thước đo biên tập.
- Steph Zinn, a16z Frontier — [The habits of AI writing](https://a16zfrontier.substack.com/p/the-habits-of-ai-writing-and-what), 22-08-2026. Tham khảo cách chọn cấu trúc theo công việc của bài và các trường hợp giữ định dạng.
- The Base Team — [Why Your Writing Sounds Like ChatGPT](https://the-curve.basehq.com/p/why-your-writing-sounds-like-chatgpt-and-how-to-fix-it), 02-10-2026. Tham khảo đối lập, nhịp giật ngắn và bố cục social; ưu tiên mẫu giọng riêng khi được cung cấp.
- Thảo luận Reddit [Lesser known AI writing tells](https://www.reddit.com/r/WritingWithAI/comments/1x6bpk5/lesser_known_ai_writing_tells/) và [The most frustrating AI writing habit](https://www.reddit.com/r/AIWritingLounge/comments/1xg0r3l/the_most_frustrating_ai_writing_habit_youve_had/). Dùng như phản hồi định tính về bình giải thừa, nhịp và câu kết lặp; ngày tuyệt đối chưa được xác minh từ HTML. Không suy ra xác suất nguồn gốc.

## Đọc bổ sung nguồn Việt về lối viết theo khuôn

Đọc ngày 04-11-2026, tiếp sau đợt nguồn quốc tế. Nhật ký: `docs/research/2026-11-04-vietnamese-writing-discussions.md` của repository. Phần vận dụng nằm trong [lối viết theo khuôn](formulaic-prose.md).

- Phạm Mỹ, Báo Văn Nghệ — [“Mùi” AI](https://baovannghe.vn/mui-ai-26802.html), 23-02-2026: nhận xét về các khuôn lặp trong nội dung thương mại Việt.
- Upcontent — [Kiểm tra văn bản AI](https://upcontent.vn/kiem-tra-van-ban-ai/), 23-10-2026: tham khảo phép thử thay tên và yêu cầu có dữ kiện riêng; không nhập danh sách từ cấm.
- Hoà Lương — [Hiểu về dấu gạch ngang](https://hoaluong.com/hieu-ve-dau-gach-ngang-de-khong-con-hoang-mang/), chưa xác minh ngày: tham khảo chức năng dấu câu qua tình huống biên tập; không áp quy tắc cấm theo ký tự.
- VOZ — [Cảm thấy khó chịu với content từ AI](https://voz.vn/t/cam-thay-kho-chiu-voi-content-tu-ai.1104978/), 26–27-05-2025: phản hồi về văn dài, lặp và quảng cáo chen ngang; không dùng để xác định ai viết.
- Pnghuy, Tinh tế — [Trải nghiệm One UI 6.1](https://tinhte.vn/thread/trai-nghiem-samsung-one-ui-6-1-tren-galaxy-s23.3774246/), 30-03-2024: nhận xét về preset giữ cùng khuôn, giới hạn ở trải nghiệm thời điểm đó.

## Giới hạn vận dụng

Các nguyên tắc về lược chủ ngữ, phép lặp, kết hợp từ và quyền giảm cường điệu trong [naturalness](naturalness.md) là quyết định biên tập của dự án dựa trên việc đọc và đối chiếu ví dụ, không được gán thành kết luận thực nghiệm của các nguồn trên. Hai bài báo không đủ đại diện cho văn viết Việt Nam. Cần review độc lập theo vùng miền, ngành và kênh trước khi công bố mức cải thiện.
