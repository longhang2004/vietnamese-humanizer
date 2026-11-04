# Cải thiện văn phong qua bài viết cùng chủ đề

Đề xuất nghiên cứu ngày 3 tháng 11 năm 2026. Dự án có thể học dần bằng cách đọc nguồn có tác giả, tạo brief, cho agent viết độc lập, biên tập và kiểm trên chủ đề mới. Mục tiêu là cập nhật hướng dẫn, ví dụ và bộ đánh giá. Quy trình này chưa huấn luyện hay cập nhật trọng số model.

Xem [danh mục nhóm văn phong cần khảo sát](style-catalog.md) và [vòng thử đã thực hiện](research/2026-11-03-same-topic-pilot.md). Pilot là công việc development, không được đưa vào benchmark. Bộ 124 case hiện tại có thêm 12 tình huống riêng từ [đợt khảo sát lối viết theo khuôn](research/2026-11-04-formulaic-prose.md), cùng 18 tình huống từ [đợt bổ sung hành chính, social và marketing](research/2026-11-04-administrative-social-marketing.md).

## Hai câu hỏi cần tách

**Học cách viết:** đọc nhiều bài cùng chủ đề/thể loại để nhận ra cách tổ chức thông tin, nhịp, xưng hô, mức trực tiếp và lựa chọn chi tiết. Một bài hay là một cách xử lý tình huống, không phải đáp án duy nhất.

**Đo hiệu quả biên tập:** dùng cùng brief và cùng bản nháp để so sánh cách sửa giữa các phiên bản. Khi đánh giá hệ thống rewrite, không để mỗi phiên bản tự viết một bài đầu vào khác nhau rồi quy mọi khác biệt cho chất lượng biên tập.

## Một vòng làm việc

1. **Chọn chủ đề và nhu cầu.** Ghi người đọc, mục đích, kênh, quan hệ, giọng, mức sửa và thông tin phải giữ. “Giới thiệu một buổi đổi sách” có thể thành bản tin, lời mời, hội thoại hoặc lời dẫn; mỗi loại có tiêu chí khác.
2. **Đọc nguồn có xuất xứ.** Nên lấy vài tác giả và vài đơn vị xuất bản trong cùng nhóm. Lưu URL, tiêu đề, byline/đơn vị biên tập, ngày xuất bản/cập nhật, ngày đọc, ngôn ngữ, thể loại, và trạng thái quyền sử dụng. Byline cùng thời điểm xuất bản là bằng chứng quy nguồn, chưa xác minh được quá trình viết từng câu. Không dùng detector để kết luận nguồn người/AI.
3. **Tạo brief bằng lời riêng.** Cùng chủ đề có thể dùng tình huống giả định với dữ kiện mới để kiểm khả năng vận dụng. Nếu dùng sự kiện thật, chỉ đưa dữ kiện đã đối chiếu, ghi nguồn cho từng dữ kiện. Tách `confirmed_facts`, `unknowns`, yêu cầu biên tập và phần nào được xuất hiện trong bài. Không biến điều chưa biết thành một lời phủ định.
4. **Cho writer viết baseline.** Writer nhận brief, chưa nhận bài mẫu hoặc hướng dẫn đang thử. Ghi nguyên prompt, output, công cụ, provider/model, cấu hình, thời gian và lỗi. Dùng subagent, OpenCode hay CLI khác đều cần cùng hợp đồng dữ liệu; tên công cụ không tự đại diện cho một model khác.
5. **Biên tập có lý do.** Editor đọc nguồn và hướng dẫn, sửa từng bản nháp; giữ cả bản gốc. Ghi những quyết định có thể vận dụng lại: đổi cấu trúc gì, giải quyết vấn đề nào, dựa vào dữ kiện nào. Cho phép `no_change`. Không lấy việc giống câu chữ tác giả nguồn hoặc đổi nhiều chữ làm mục tiêu.
6. **Review riêng.** Cho reviewer khác đọc brief và các bản ẩn nhãn. Kiểm dữ kiện trước, rồi xét mạch, giọng, độ tự nhiên và sửa thừa. Giữ bất đồng và trường hợp hòa. Reviewer AI giúp tìm lỗi nhanh; review bản ngữ độc lập vẫn là một lớp riêng.
7. **Cập nhật hẹp, kiểm lại rộng hơn.** Chỉ thêm một hướng dẫn khi nó giải thích được vấn đề và có phản ví dụ cần giữ nguyên. Kiểm trên nhóm chủ đề/tác giả chưa dùng để viết hướng dẫn. Nếu thay đổi chỉ tốt cho bài vừa đọc, giữ dưới dạng quan sát riêng.

## Thiết kế so sánh

Ở development, có thể dùng ba nhánh trên cùng bản nháp:

- Baseline với hướng dẫn hiện hành, giữ phiên bản model và cấu hình sinh.
- Hướng dẫn mới rút ra từ nguồn, không cung cấp nguyên bài mẫu trong lần sửa.
- Hướng dẫn mới kèm ví dụ ngắn có quyền sử dụng rõ, nếu muốn đo riêng tác dụng của ví dụ.

Đọc mẫu rồi sửa ngay chỉ là thử nghiệm khám phá. Chia development/test theo cụm chủ đề, tác giả và bài gốc; các bài đăng lại hoặc bản diễn đạt lại của một nguồn ở cùng một cụm. Với tình huống giả định, nhóm các biến thể của cùng brief lại. Đóng băng hướng dẫn trước khi dùng tập giữ lại; không sửa prompt theo lỗi test rồi tiếp tục gọi đó là test chưa thấy.

Khi báo cáo, ghi số tình huống độc lập, số biến thể, số reviewer và output lỗi. Báo riêng độ phủ, lỗi bảo toàn và cảm nhận giọng; điểm trung bình không bù được lỗi bịa dữ kiện. Có thể cho người đọc chọn A/B/hòa với thứ tự xáo trước. Áp dụng [quy trình review hiện có](../benchmarks/profile-review.md) khi chuyển thí nghiệm thành batch benchmark.

## Chạy qua agent hoặc CLI

Ngày khảo sát, WSL có OpenCode `1.19.3`; `opencode run --help` có lựa chọn file, model và output JSON. Chưa chạy sinh bài bằng CLI trong đợt này. Không tìm thấy lệnh Antigravity trong PATH của Ubuntu WSL; kết quả đó không xác định tình trạng cài đặt trên Windows.

Pilot dùng subagent với `fork_turns=none` để writer không nhận lịch sử nghiên cứu. Công cụ không trả model ID/cấu hình sinh cụ thể, nên pilot ghi các trường đó là chưa biết và chưa thể tái lập đầy đủ. Với một runner chính thức, cần lưu được metadata này trước khi so sánh các model.

Mỗi runner chỉ cần nhận gói brief cố định và xuất output cùng metadata. Giữ snapshot/commit, hash prompt/skill, model ID, provider, phiên bản CLI, cấu hình, thời gian, lỗi và phạm vi tài liệu đã cung cấp. Không lưu key/token. Chạy trong thư mục thí nghiệm riêng, chỉ cung cấp tài liệu được chọn; không bật tự duyệt thao tác cho tác vụ viết. Thử một writer và một reviewer trước, tránh lặp vô hạn khi model không trả đúng định dạng.

## Nguồn và quyền sử dụng

Danh mục nguồn đọc nằm trong [style catalog](style-catalog.md). Lưu liên kết và quan sát bằng lời riêng; chưa nhập toàn văn bài báo/blog vào corpus hoặc repository. Việc một bài đọc được công khai không chứng minh quyền dùng làm dữ liệu huấn luyện hay phân phối lại. Ví dụ, Mailchimp công bố style guide dưới CC BY-NC 4.0 trên [trang giới thiệu](https://styleguide.mailchimp.com/); giấy phép đó không được chuyển thành MIT của dự án. Các hướng dẫn ở đây là đề xuất tự viết, không sao chép nội dung hướng dẫn nguồn.

Trước khi thêm trích đoạn hoặc dataset, ghi phạm vi giấy phép/cho phép tương ứng. Không gán câu AI tự viết cho tác giả nguồn, không làm giả trải nghiệm cá nhân và không lưu hội thoại riêng tư chưa được cho phép. Chỉ đề xuất giọng theo đặc điểm chung và mục đích sử dụng, không dùng tên một tác giả làm tiêu chí đạt.
