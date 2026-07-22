# Ví dụ chọn lọc

## Cần sửa

Input: "Giải pháp này đóng vai trò quan trọng trong việc giúp nhóm nâng cao hiệu suất."

Output: "Giải pháp này giúp nhóm làm việc nhanh hơn."

Chỉ dùng output nếu "hiệu suất" trong ngữ cảnh thực sự là tốc độ. Nếu hiệu suất còn gồm chi phí hoặc độ chính xác, giữ nghĩa rộng hơn.

Input: "Trong bài viết này, chúng ta sẽ cùng tìm hiểu cách bộ nhớ đệm giảm số lần ứng dụng phải đọc lại cùng một dữ liệu."

Output: "Bộ nhớ đệm giảm số lần ứng dụng phải đọc lại cùng một dữ liệu."

Input: "Trong bối cảnh kỷ nguyên số không ngừng phát triển, doanh nghiệp cần đổi mới."

Output: "Doanh nghiệp cần đổi mới." Chỉ thay bằng một thay đổi cụ thể nếu input hoặc context thực sự cung cấp thay đổi đó.

## Không nên sửa

Input: "Nghiên cứu có thể chưa phản ánh nhóm người trên 65 tuổi vì mẫu chỉ có 18 người ở độ tuổi này."

Output: giữ nguyên. Câu cụ thể, hedge có lý do và số liệu cần thiết.

Input: "Quý khách vui lòng mang theo căn cước công dân khi nhận thẻ."

Output: giữ nguyên nếu đây là thông báo chính thức của ngân hàng. Không đổi thành "Bạn nhớ mang CCCD nhé".

Bộ 103 ví dụ có metadata theo domain nằm trong `examples/examples.jsonl` của repository.
