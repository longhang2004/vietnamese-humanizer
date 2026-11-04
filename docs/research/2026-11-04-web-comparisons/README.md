# Các cặp ví dụ AI trên web

Ngày chạy: 04-11-2026. Đây là các lượt biên tập thật do hai Codex subagent riêng biệt thực hiện, dùng model kế thừa phiên làm việc. Công cụ không công bố mã phiên bản provider hoặc seed; không gán một tên model cụ thể thay cho thông tin còn thiếu.

- [Briefs](briefs.json): sáu đoạn giả định và yêu cầu biên tập, được chốt trước hai lượt sinh.
- [Không nạp bộ skill tiếng Việt](baseline.json): agent chỉ đọc briefs, được yêu cầu trả lời tốt nhất theo cách thông thường, không cố viết kém hoặc tạo dấu hiệu AI.
- [Có nạp bộ skill tiếng Việt](with-skills.json): cùng briefs, thêm humanizer và reference theo profile tại commit `845c3795f26346c4f5801e35365d65ff939a8e08`.

Hai bên đều chịu chỉ dẫn chung của môi trường Codex. “Không nạp skill” ở đây chỉ bộ Vietnamese Writing Skills; không có nghĩa model không chịu bất kỳ hướng dẫn nào. Mỗi agent xử lý sáu case trong một context riêng; các case không phải các lượt lấy mẫu độc lập. Không dùng đầu ra bên này làm đầu vào bên kia, không chạy lại để chọn bản thuận lợi.

Toàn bộ sáu cặp được đưa lên web nguyên văn. Một số kết quả rất gần nhau; điều đó vẫn được giữ lại. Chủ đề kỹ thuật được chọn làm ví dụ mở đầu vì người dùng yêu cầu hướng web thiên về kỹ thuật. Người xem có thể đổi sang mọi chủ đề còn lại, xem yêu cầu và đoạn gốc.

`scripts/export_web_comparisons.py` chỉ gộp dữ liệu và hash nguồn vào `web/frontend/content/comparisons.json`. Nó không sinh hoặc biên tập đầu ra. Chạy với `--check` để phát hiện thay đổi chưa đồng bộ.

Đây là ví dụ minh họa chức năng, không phải benchmark kiểm soát model, chứng minh hơn/kém, đo hiệu quả chung hoặc đánh giá bởi người bản ngữ độc lập. Không nhập các ví dụ này vào corpus hay bộ 124 benchmark case.
