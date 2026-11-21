# Giọng marketing, phủ định và chú thích

Đọc ngày 22-11-2026. Khảo sát các vị trí người đọc gặp khi xem một đề nghị, gồm lời mở, mô tả lợi ích, nút hành động và chú thích. Mẫu nhỏ giúp chọn nguyên tắc biên tập. Các trang thương hiệu cho thấy câu chữ đã công bố. Tên tác giả chỉ được ghi ở nguồn có công bố. Các tình huống kiểm chứng được soạn riêng.

| Nguồn | Phần đã đọc và cách vận dụng |
| --- | --- |
| [Apple Việt Nam, iPhone](https://www.apple.com/vn/iphone/) | Phần iPhone và Apple Watch mở bằng một câu hỏi về việc để quên điện thoại rồi giải đáp bằng tính năng tìm. Giữ câu hỏi khi lợi ích ngay sau đó giải quyết tình huống người đọc nhận ra. |
| [Apple Việt Nam, so sánh iPhone](https://www.apple.com/vn/iphone/compare/) | Dòng thông số pin nêu mức tối đa và hoạt động đo. Chú thích trình bày cách thử và yếu tố làm kết quả thay đổi. Giữ bối cảnh cần để hiểu con số trong lời chính. |
| [Spotify Premium Việt Nam](https://www.spotify.com/vn-vi/premium/) | Khoảng dùng thử và giá xuất hiện trên nút. Giá sau ưu đãi và điều kiện đối tượng xuất hiện ngay bên dưới. Phần lợi ích dùng phủ định có nghĩa khi nói về quảng cáo và việc nghe ngoại tuyến. |
| [MoMo và Coca-Cola](https://www.momo.vn/coke) | Lời mở mùa hè có câu cảm thán. Danh sách thẻ quà lại dùng cụm ngắn nêu mức ưu đãi và cách dùng. Cùng một trang có thể thay nhịp theo chức năng của từng phần. |
| [Biti's, thông báo voucher 24-04-2025](https://bitis.com.vn/blogs/news/bitis-tang-voucher-giam-50k-ky-niem-50-nam-giai-phong-mien-nam) | Điều kiện không cộng dồn xuất hiện trong phần thông tin voucher. Dấu sao dẫn đến dòng liên hệ hỗ trợ. Ưu đãi lịch sử đã hết hạn. |
| [Hồng Anh, quản lý thương hiệu Neptune, trả lời Đỗ Kim](https://www.brandsvietnam.com/congdong/topic/8823-bsi-case-study-neptune-chien-dich-hieu-de-yeu-thuong) | Các thông điệp có vần đi với hình ảnh về việc nhà để gắn ý chính vào tình huống dễ nhớ. Đây là giải thích của người làm chiến dịch về vai trò của vần trong tổng thể quảng cáo. |
| [Joanna Wiebe, Copyhackers](https://copyhackers.com/2015/09/asking-questions/) | Một thử nghiệm popup đặt câu hỏi bán sách cạnh một tiêu đề giới thiệu. Bản giới thiệu thu được nhiều đăng ký hơn trong lần thử đó. Vận dụng bằng cách xét câu hỏi cùng người đọc và phần thông tin theo sau. |
| [FTC, Advertising FAQs](https://www.ftc.gov/business-guidance/resources/advertising-faqs-guide-small-business) | Tham khảo nguyên tắc dễ nhìn thấy và gần tuyên bố cần bổ nghĩa. Đây là nguồn của Hoa Kỳ, dùng để tham khảo cách bố trí thông tin. |

## Quyết định biên tập

- Giữ kiểu mở có chức năng trong giọng thương hiệu. Câu hỏi cần chạm một tình huống và được giải đáp. Cảm thán có thể báo một tin vui. Giá, mốc và cách tham gia có thể viết trực tiếp trong cùng bài.
- Bỏ phủ định dùng để trì hoãn chi tiết hữu ích. Giữ phủ định nêu quyền lợi, trạng thái hoặc giới hạn. Chỉ đổi sang cách nói khẳng định nếu không làm rộng hay hẹp nghĩa.
- Cho người đọc thấy điều kiện ảnh hưởng giá, quyền lợi hoặc khả năng mua trong cùng khối với lời mời, trước thao tác. Giữ dấu chú thích đi cùng nội dung tương ứng khi dùng cho cách đo, nguồn hoặc thông tin tra cứu.

## Kiểm chứng phát triển

Năm case mới nằm trong [bộ benchmark marketing](../../benchmarks/cases/marketing-editorial-styles.jsonl). Hai lượt dùng agent mới với cùng model và năm đề giả định. Agent chỉ đọc hướng dẫn và đề biên tập, không đọc nhãn dự kiến. Lượt dùng v0.6.1 đã giữ các đoạn phù hợp, bỏ câu đối lập đệm ở case đèn và đưa điều kiện nhận túi lên trước nút. Riêng tiêu đề nhận túi vẫn đứng thành một khối độc lập với điều kiện. Đây là tình huống giúp kiểm xem hướng dẫn mới có gắn điều kiện chặt hơn với lời mời trên màn hình nhỏ hay không.

Lượt dùng hướng dẫn mới giữ nguyên ba đoạn đã rõ và bỏ câu phủ định đệm ở case đèn. Ở case túi, lời mời và điều kiện nhận nằm trên hai dòng liền nhau trước nút. Dòng ghi nguồn ảnh vẫn đứng riêng. Hai lượt đều giữ dữ kiện và xử lý đúng các trường hợp cần sửa hay giữ. Đây là kiểm tra định tính trên đề phát triển, chưa đo tỷ lệ chuyển đổi hoặc chất lượng qua người chấm độc lập.
