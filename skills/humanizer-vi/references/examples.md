# Ví dụ chọn lọc

## Cần sửa

Input: "Giải pháp này đóng vai trò quan trọng trong việc giúp nhóm nâng cao hiệu suất."

Output: "Giải pháp này giúp nhóm làm việc nhanh hơn."

Chỉ dùng output nếu "hiệu suất" trong ngữ cảnh thực sự là tốc độ. Nếu hiệu suất còn gồm chi phí hoặc độ chính xác, giữ nghĩa rộng hơn.

Input: "Trong bài viết này, chúng ta sẽ cùng tìm hiểu cách bộ nhớ đệm giảm số lần ứng dụng phải đọc lại cùng một dữ liệu."

Output: "Bộ nhớ đệm giảm số lần ứng dụng phải đọc lại cùng một dữ liệu."

Input: "Trong bối cảnh kỷ nguyên số không ngừng phát triển, doanh nghiệp cần đổi mới."

Output: "Doanh nghiệp cần đổi mới." Chỉ thay bằng một thay đổi cụ thể nếu input hoặc context thực sự cung cấp thay đổi đó.

Input: "Chuẩn bị sớm là cần thiết. Việc gửi agenda trước là quan trọng. Việc tham dự đúng giờ là hữu ích."

Output: "Chuẩn bị sớm là cần thiết. Gửi agenda trước là quan trọng; tham dự đúng giờ cũng hữu ích." Giữ ba mức đánh giá khác nhau, không thay chúng bằng một lời khuyên chung.

Input: "Chúng tôi vô cùng thấu hiểu sự thất vọng sâu sắc mà vấn đề này đã gây ra cho quý khách."

Khi tác giả chọn giảm cường điệu (`reduce_hype=true`): "Chúng tôi hiểu vấn đề này khiến quý khách thất vọng." Không thêm lời hứa xử lý. Nếu chưa được phép làm nhẹ cường độ cảm xúc, góp ý về giọng công thức thay vì chỉ đổi "vô cùng" thành "rất".

Input: "Một giải pháp đột phá mang đến trải nghiệm tuyệt vời cho mọi người dùng."

Context: ứng dụng tự lưu và đồng bộ bản nháp, chưa có bằng chứng cho các nhận định bao quát. Chọn `review_comment`: các tính năng chưa đủ chứng minh "đột phá" hoặc "mọi người dùng"; tác giả cần cung cấp căn cứ hoặc quyết định có bỏ các nhận định đó không. Nhận xét này không phải bản thay thế.

## Không nên sửa

Input: "Nghiên cứu có thể chưa phản ánh nhóm người trên 65 tuổi vì mẫu chỉ có 18 người ở độ tuổi này."

Output: giữ nguyên. Câu cụ thể, hedge có lý do và số liệu cần thiết.

Input: "Quý khách vui lòng mang theo căn cước công dân khi nhận thẻ."

Output: giữ nguyên nếu đây là thông báo chính thức của ngân hàng. Không đổi thành "Bạn nhớ mang CCCD nhé".

Bộ 103 ví dụ có metadata theo domain nằm trong `examples/examples.jsonl` của repository.
