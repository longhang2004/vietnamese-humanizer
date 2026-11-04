# Pilot cùng chủ đề: một buổi đổi sách

Thực hiện ngày 3 tháng 11 năm 2026. [Dữ liệu nguyên bản và bản sửa](2026-11-03-same-topic-pilot.json) gồm prompt writer, bốn bản nháp, bốn bản sau biên tập, mapping A/B và phản hồi reviewer. Không đưa dữ liệu này vào `examples/`, `benchmarks/cases/` hoặc kết quả baseline.

## Đã thực hiện

1. Agent chính đọc bài về hội sách của [Nhật Nam](https://baochinhphu.vn/hoi-sach-xuan-2018-hoi-sach-cu-lon-nhat-nam-102235514.htm) và bài về đọc sách của [Nguyễn Nhật Ánh](https://tuoitre.vn/nha-van-nguyen-nhat-anh-toi-me-doc-sach-tu-chuyen-ke-cua-ba-20190420081641818.htm), cùng các hướng dẫn được ghi trong [style catalog](../style-catalog.md). Quan sát chỉ áp dụng thử, không sao văn hoặc mô phỏng giọng riêng của tác giả.
2. Tạo tình huống giả định cùng chủ đề sách với tên, thời gian, số chỗ và quy định mới. Đây là cùng chủ đề, không phải viết lại tin sự kiện năm 2018.
3. Gọi subagent writer qua `collaboration.spawn_agent`, dùng `fork_turns=none`, chỉ cung cấp brief. Writer không được cung cấp bài nguồn hay skill; tạo bản tin, bài mời social, lời dẫn nói và bài mời dí dỏm.
4. Agent chính biên tập thủ công sau khi đọc nguồn và hướng dẫn dự án. Không gọi rewrite API, OpenCode hay Antigravity để tạo các bản này.
5. Gọi subagent reviewer khác, cũng không kế thừa lịch sử, cung cấp brief và các bản ẩn nhãn A/B. Giữ nguyên phản hồi dạng định tính; không tạo điểm số hoặc kết quả review con người.

## Điều quan sát được

| Bản | Quyết định biên tập | Nhận xét của reviewer AI |
| --- | --- | --- |
| Bản tin | `no_change`: giữ nguyên bản nháp | Hai bản giống nhau và phù hợp mục đích |
| Social | Bỏ việc tự xác định nơi diễn ra sự kiện và “Chủ nhật này”; gọn lời nhắc đăng ký | Ưu tiên bản sửa; ghi hai chỗ suy diễn trong bản nháp |
| Lời dẫn nói | Viết giờ/số theo cách đọc thành tiếng, bỏ phần nhắc hạn lặp trong đoạn ngắn | Ưu tiên bản sửa; vẫn công nhận lời chào/nhắc lại có thể hợp tình huống |
| Dí dỏm nhẹ | Giữ hình ảnh sách biết lên lịch, bỏ câu thêm gượng và nêu Chủ nhật rõ trong phần thông tin | Ưu tiên bản sửa; chưa có người đọc thật kiểm mức hài hước |

Thông tin “đơn vị tổ chức” không tự xác nhận “địa điểm diễn ra”. “Chủ nhật” chưa xác định ngày cụ thể hoặc có phải Chủ nhật gần nhất hay không. Hai chi tiết thêm cần tác giả xác nhận theo brief đang thử; chưa chứng minh chúng sai ngoài đời hoặc mọi bài social có vấn đề này. Sự thiếu rõ ràng của brief cũng cần được xem lại trước khi đặt nhãn benchmark.

Nguồn người viết giúp đặt câu hỏi về cấu trúc, nhịp và mức sinh động. Trong pilot này, căn cứ phát hiện hai suy diễn là brief, không phải bài nguồn. Các lựa chọn viết số thành chữ và bỏ câu gượng là phán đoán biên tập, chưa có thí nghiệm chứng minh nguồn đọc gây ra cải thiện. Một liên tưởng vui có thể giữ lại khi nó phục vụ giọng đã yêu cầu và không bị đọc thành cam kết thực tế.

## Vấn đề của brief

Prompt ban đầu trộn điều chưa biết về đăng ký trực tuyến với những dữ kiện cần đưa vào bài, nên cả bốn bản đều nhắc trạng thái thiếu thông tin đó. Đây cũng là vấn đề thiết kế brief, không nên mặc định chấm thành lỗi writer. Pilot giữ nguyên thông tin trong mọi bản sửa để không thay yêu cầu giữa chừng.

Vòng sau nên tách dữ kiện công bố, điều chưa biết và câu hỏi cho tác giả. Nếu không có thông tin đăng ký online, writer phải tránh bịa link hoặc khẳng định “không có đăng ký online”; việc có đưa trạng thái chưa biết vào bài hay trả trong comments cần được nêu trước.

## Giới hạn và bước tiếp

- Một tình huống với bốn biến thể phụ thuộc; đây là development, không phải tập test chưa thấy.
- Writer, editor, reviewer đều là AI. Công cụ không cung cấp model ID/cấu hình cụ thể; không khẳng định chúng là ba model khác nhau. Reviewer không biết nhãn phiên bản nhưng nhận hướng dẫn bảo toàn rõ hơn prompt writer về địa điểm/ngày; A/B được sắp cố định. Chưa phải thử nghiệm mù được kiểm soát đầy đủ.
- Chưa có dữ liệu về lời nói tự phát, lượt hội thoại thật, marketing bán hàng hoặc nhiều loại hài hước. Không tính tỷ lệ thắng từ bốn nhận xét này.
- Không xác minh quyền sao chép toàn văn các bài nguồn; chỉ lưu liên kết và quan sát bằng lời riêng. Dữ kiện và bản nháp pilot là giả định mới.

Vòng tiếp theo cần nhiều chủ đề độc lập, brief có cấu trúc, prompt/model được lưu đầy đủ, thứ tự chấm xáo trước và reviewer bản ngữ. Một hướng dẫn mới chỉ nên được đưa vào skill sau khi qua phản ví dụ cần giữ nguyên và tình huống chưa dùng để thiết kế nó. Xem [quy trình đề xuất](../style-learning-loop.md).
