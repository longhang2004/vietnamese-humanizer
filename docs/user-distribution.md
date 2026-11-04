# Phân phối cho người không viết code

Trang `/start` hướng dẫn chọn chatbot, chọn một trong bốn nhu cầu và tải hoặc sao chép hướng dẫn. Trang dùng dữ liệu tĩnh, không cần backend hoạt động để tải tệp hay sao chép prompt. Người dùng dán văn bản vào chatbot của họ; trang này không thu thập văn bản cần biên tập.

## Các gói được xuất

Nguồn chung là `skills/`, `distribution/catalog.json`, icon của dự án, giấy phép và metadata phiên bản. Catalog chứa tên dễ hiểu, mô tả kích hoạt ngắn, yêu cầu mẫu và ngày đối chiếu tài liệu nền tảng. Nội dung skill và reference vẫn lấy từ thư mục skill. `quick_start` là bản hướng dẫn rút gọn; nó không thay thế đầy đủ reference của bốn skill.

| Tệp trong `web/frontend/public/downloads/` | Mục đích |
| --- | --- |
| `claude/<skill-id>.zip` | Mỗi ZIP có một thư mục gốc trùng tên skill, gồm `SKILL.md`, reference, asset Markdown và `LICENSE.txt` |
| `gemini/<skill-id>.zip` | `SKILL.md` ngay gốc ZIP cùng reference, asset Markdown và giấy phép |
| `chatgpt/vietnamese-writing-skills.zip` | Gói plugin chuẩn bị nộp: manifest, bốn skill, icon và giấy phép; chưa có MCP hoặc đăng ký listing |
| `huong-dan-tieng-viet.md` | Bốn skill và reference gộp trong một tài liệu; liên kết nội bộ chuyển thành anchor trong tệp |
| `yeu-cau-bien-tap.txt` | Yêu cầu rút gọn để thử nhanh |
| `BAT-DAU.txt` | Cách cài và dùng khi nhận tệp qua GitHub Release |
| `manifest.json` | Metadata, tên nhu cầu, hash nguồn và checksum/kích thước từng tệp |

Các gói chỉ chứa hướng dẫn, không cần cài Python/Node hoặc cung cấp API key. Hành vi phụ thuộc model và nền tảng; việc nạp file không chứng minh chất lượng biên tập.

## Sinh và kiểm tra

Từ repository đã cài development dependencies:

```bash
python scripts/export_user_packs.py
python scripts/export_user_packs.py --check
```

Có thể đặt `--root PATH` hoặc `--output PATH` khi chuẩn bị một bộ riêng. Exporter chỉ lấy `SKILL.md` và các tệp `.md`/`.txt` trong references/assets của bốn skill đã định danh; bỏ qua tệp/thư mục ẩn, không lấy cấu hình tài khoản, corpus, benchmark hoặc file người dùng ngoài các thư mục đó. Link reference chưa được đóng gói sẽ làm build thất bại.

Mô tả kích hoạt trong bản xuất dùng `description` của catalog để đáp ứng giới hạn 200 ký tự của Claude; `summary` là mô tả tác vụ dùng trên giao diện. Body của `SKILL.md` và reference giữ nội dung nguồn. ZIP có thứ tự, timestamp và quyền tệp cố định, không nén để byte ổn định giữa các phiên bản Python/zlib. Text được chuẩn hóa xuống dòng LF. Hash giúp kiểm tra đồng bộ, không phải chữ ký xác thực hay chứng nhận chất lượng.

Commit các tệp sinh cùng thay đổi nguồn. CI root và Web CI kiểm `--check`; không cần Python trong quá trình build/deploy frontend vì bộ tải đã được tạo sẵn. Nếu đổi nguồn, cần chạy lại exporter trước khi push. Chế độ check cũng báo tệp thừa cũ; xem xét và xóa chúng khi chủ động đổi tên gói.

## Phát hành

Workflow release kiểm đồng bộ, build Python wheel/sdist và tạo `vietnamese-writing-skills-user-packs.zip` từ toàn bộ download. Bộ tải là artifact riêng; chỉ wheel/sdist đi tới PyPI. GitHub Release đính kèm thêm ZIP cho người dùng. Trang web phục vụ các đường dẫn `/downloads/...` từ cùng các tệp đã kiểm tra.

Plugin ChatGPT có manifest portable và icon, chưa được nộp hoặc chấp thuận trong Plugins Directory. Trang mặc định cung cấp yêu cầu dùng nhanh và ghi đúng trạng thái. Sau khi listing thật đã phát hành, đặt URL chính thức vào `chatgpt_install_url` trong catalog rồi sinh lại; trang sẽ hiện nút cài. Tạo gói ZIP không tự xuất bản plugin. Không dùng link tải ZIP làm link cài đặt.

Để chuẩn bị submission, tải gói trong `chatgpt/`, kiểm metadata publisher, icon, mô tả và các reference. Cần thực hiện kiểm tra nạp skill trên tài khoản thử, hoàn tất các yêu cầu xác minh/xét duyệt hiện hành và kiểm đường cài trên các surface được hỗ trợ. Không thêm MCP vào gói này nếu chưa quyết định kiến trúc server và đường nâng cấp; tài liệu OpenAI hiện nêu hạn chế thêm MCP vào một plugin skills-only đã có.

## Đối chiếu nền tảng

Đối chiếu ngày 4 tháng 11 năm 2026; không tự động giả định giao diện đã rollout tới mọi tài khoản.

- [OpenAI — package a plugin](https://developers.openai.com/plugins/build/plugins): manifest portable, thư mục skill và metadata trình bày.
- [OpenAI — upload and submit](https://developers.openai.com/plugins/deploy/submission): quy trình kiểm tra, xét duyệt và phát hành; gói hiện chỉ mới chuẩn bị cấu trúc.
- [Claude — create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills): ZIP có thư mục skill gốc, mô tả tối đa 200 ký tự và reference trong thư mục.
- [Claude — use skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude): upload/bật skill và yêu cầu về Code execution and file creation.
- [Google — create and manage skills](https://support.google.com/gemini/answer/17094296): upload `SKILL.md` hoặc folder/ZIP ở web; reference đi cùng skill.
- [Google — chuyển Gems sang skills](https://support.google.com/gemini/answer/18560919): rollout theo loại tài khoản; dùng yêu cầu rút gọn khi chưa có giao diện Skills.

## Kiểm thử tiếp với người dùng

Nhờ 5–10 người không biết code chọn chatbot, cài hoặc dùng prompt rồi sửa một đoạn của họ. Ghi nơi mắc, thời gian tới kết quả đầu tiên và khả năng tự tìm cách cập nhật. Không thu thập nội dung văn bản nếu không cần và chưa được cho phép. Hiện đã có kiểm thử tự động gói và giao diện; chưa có kết quả usability từ người tham gia thật hoặc xác nhận import trên mọi nền tảng.
