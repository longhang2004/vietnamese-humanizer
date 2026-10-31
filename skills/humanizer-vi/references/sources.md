# Nguồn đọc về văn phong

Đọc ngày 31 tháng 10 năm 2026. Các nguồn dưới đây có tên tác giả hoặc người trả lời được công bố. Đây là cơ sở quy nguồn, không phải chứng nhận cách từng câu được sản xuất. Dự án không sao chép bài báo, nhập chúng làm corpus hay mô phỏng giọng riêng của tác giả. Ví dụ và benchmark mới do coding agent tự viết, chưa được reviewer bản ngữ độc lập duyệt.

## Tiếng Việt được người viết sử dụng

- Hoàng Thu Phố thực hiện phỏng vấn Nguyễn Ngọc Tư, [Viết là cách tôi giao lưu với bạn đọc](https://nhandan.vn/viet-la-cach-toi-giao-luu-voi-ban-doc-post348644.html), Nhân Dân/Thời Nay, 31-01-2019. Quan sát của dự án: nhịp câu không đều vẫn theo được vì đối tượng và lập trường xuyên suốt; cách xưng hô và sắc thái cá nhân không cần chuẩn hóa thành giọng doanh nghiệp. Đây là mẫu hội thoại đã biên tập, không đại diện cho mọi văn nói hoặc mọi vùng miền.
- Nam Kha, [Viết sao cho hay, viết gì cho chất?](https://muctim.tuoitre.vn/viet-sao-cho-hay-viet-gi-cho-chat-101230629160346324.htm), Mực Tím/Tuổi Trẻ, 29-06-2023; ghi nhận chia sẻ của nhà báo Nguyễn Khắc Cường. Bài bàn về chất liệu quan sát và việc giữ mạch khi viết. Vận dụng của dự án: ưu tiên chi tiết đã có trong input/context và kiểm tra mạch đoạn. Với tác vụ biên tập, việc bịa thêm chi tiết để làm sinh động vẫn bị cấm.

## Nghiên cứu để thiết kế đánh giá

- Zheng-Yu Huang và Richard Tzong-han Tsai, [Evaluating Pragmatic Appropriateness in English–Vietnamese Machine Translation with Dyadic Profiles](https://aclanthology.org/2026.wmt-main.16/), WMT 2026. Nghiên cứu nhỏ phân biệt câu đúng/tự nhiên với câu hợp quan hệ người gửi–người nhận. Không phát hiện cải thiện tổng thể có ý nghĩa thống kê từ việc thêm profile; một số phép so sánh cho thấy khác biệt phụ thuộc quan hệ. Dự án tham khảo cách đánh giá riêng tính phù hợp quan hệ và so sánh cặp; bộ hiện tại chưa tái lập thử nghiệm đảo vai và không coi profile là bảo đảm chất lượng.
- Sang Quang Nguyen và Kiet Van Nguyen, [A Large-Scale Benchmark for Vietnamese Sentence Paraphrases](https://aclanthology.org/2025.findings-naacl.59/), Findings of NAACL 2025. ViSP là nghiên cứu paraphrase ở cấp câu với sinh tự động và đánh giá thủ công. Dự án tham khảo việc đánh giá nhiều cách diễn đạt; không nhập dataset hoặc xem điểm tương đồng là bằng chứng giữ nguyên mọi sắc thái.

## Phạm vi suy luận

Các nguyên tắc về lược chủ ngữ, phép lặp, kết hợp từ và quyền giảm cường điệu trong [naturalness](naturalness.md) là quyết định biên tập của dự án dựa trên việc đọc và đối chiếu ví dụ, không được gán thành kết luận thực nghiệm của các nguồn trên. Hai bài báo không đủ đại diện cho văn viết Việt Nam. Cần review độc lập theo vùng miền, ngành và kênh trước khi công bố mức cải thiện.
