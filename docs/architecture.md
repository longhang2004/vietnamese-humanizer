# Kiến trúc

Repository tách dữ liệu ngôn ngữ, logic deterministic và quy trình review. Mỗi lớp chỉ xử lý phần có thể kiểm chứng.

## Agent Skills

Bốn thư mục trong `skills/` chứa quy trình ra quyết định và kiến thức biên tập theo cấu trúc biên tập 2 pha (Pha 1 chẩn đoán & biên tập tự nhiên; Pha 2 đối chiếu bảo toàn). `SKILL.md` giữ hướng dẫn cốt lõi; reference chỉ nạp khi cần, còn ghi chú nguồn đọc tác giả nằm riêng tại `docs/sources.md`. Agent hoặc reviewer thực hiện bản viết lại vì quyết định sửa cần xét mục đích, độc giả, register, thuật ngữ, chỗ mơ hồ và dữ kiện của toàn văn bản.

Web rewrite nhận `context`, `style` (bao gồm `voice_sample` tùy chọn để neo giọng viết) và `profile`. Backend nạp `SKILL.md` cùng danh sách reference cố định theo skill và chọn lọc theo ngữ cảnh (chỉ nạp `registers.md`, `formulaic-prose.md`, `examples.md`, `workflow.md`, `conversational.md` hoặc `humor-and-satire.md` khi tín hiệu phát hiện, `profile`, `edit_level`, `channel` hoặc ngữ cảnh cần tới); đường dẫn reference không lấy từ request. Kết quả model được parse theo schema (kèm trường `preservation_check` nội bộ trước `rewrite`), chuẩn hóa `no_change` về nguyên văn input, chạy hậu kiểm token bảo toàn (`audit_preserved_tokens` cho code, URL, email, số/ngày/tỷ lệ khi `clean_rewrite` trừ `style-guide-vi` hoặc `spoken_script`) và tách `comments` khỏi replacement text. Đây là kiểm tra giao thức và rà soát bề mặt, không phải kiểm chứng bảo toàn ngữ nghĩa tuyệt đối.

`style.profile` chọn `preserve` (mặc định), `plain`, `business`, `technical`, `administrative`, `social` hoặc `marketing`. Backend dùng allowlist để nạp `writing-profiles.md` và đúng một reference theo profile từ tài nguyên `humanizer-vi` đã đóng gói, kể cả khi skill đang chọn là `grammar-checker-vi`, `style-guide-vi` hay `translationese-cleaner-vi`; phạm vi skill vẫn giữ nguyên. Profile độc lập với `channel`, `register`, `edit_level` và `voice_sample`. Frontend gửi lựa chọn này cùng style và hủy hiển thị kết quả cũ hoặc đến trễ khi người dùng thay đổi văn bản, mẫu giọng hay lựa chọn biên tập.

## Pattern data

Các file YAML trong `patterns/` lưu tín hiệu có thể kiểm tra hoặc gợi ý review. JSON Schema bắt buộc `finding_type`, `scope` và `aggregation`. Catalog không phải từ điển lỗi. Dù heuristic có regex ổn định, reviewer vẫn phải đánh giá tác động trong đoạn hoặc toàn tài liệu.

## Example corpus

`examples/examples.jsonl` lưu 103 cặp input/output. Mỗi dòng có `context`, `must_preserve`, `must_not_add` và `preservation_review`. Context tách khỏi input để reviewer biết output được phép dùng dữ kiện nào. Cách này tránh các giải thích mơ hồ như “chi tiết đã có trong bài”. JSON Schema kiểm cấu trúc và tham chiếu pattern, không tự chứng minh bảo toàn ngữ nghĩa.

## Python package

Logic importable nằm dưới `src/vietnamese_writing_skills/`:

- `core/` đọc resource, kiểm frontmatter, pattern, example và benchmark;
- `cli/` chứa linter, validator, benchmark runner và generator;
- `data/` là namespace cho resource được đưa vào wheel.

Các file trong `scripts/` không phải package Python. Chúng chỉ gọi `main()` từ package chính thức để giữ tương thích với command cũ.

## Package resources

Hatch đưa `patterns/`, `skills/`, `examples/` và `benchmarks/` vào `vietnamese_writing_skills/data/` trong wheel. Khi CLI chạy trong source checkout, nó dùng dữ liệu của repository để maintainer thấy thay đổi đang sửa. Ngoài checkout, lệnh đọc dữ liệu bằng `importlib.resources`. Option `--root PATH` cho phép kiểm một repository bất kỳ.

Wheel phải chứa resource vì linter và validator cần schema/YAML sau khi cài ở một môi trường khác. Chỉ đóng gói Python module sẽ làm command chạy được `--help` nhưng lỗi ngay khi xử lý văn bản.

## Deterministic validation và linter

Validator kiểm schema, ID trùng, regex, link, review status và generated docs. Linter che fenced code, inline code, URL và một số identifier trước khi phát hiện tín hiệu bề mặt. Output phân biệt error, warning, preference và heuristic; không có AI score.

Regex không đủ để humanize. Nó không biết metric có tồn tại trong nguồn hay đại từ nào phù hợp quan hệ xã hội. Nó cũng không biết câu bị động có cần trong phương pháp nghiên cứu không. Vì vậy CLI chỉ nêu vị trí và đề xuất review, không tự rewrite.

## Benchmark

Benchmark tách khỏi unit test (`benchmarks/cases/` gồm 161 case, có `style.voice_sample` tùy chọn). Case lưu input, context, constraints, must-preserve, must-not-add và blocker. Cờ `--prepare-packet` xuất gói đầu vào chấm mù (`text`, `context` đã gộp constraints, `style`) và loại bỏ hoàn toàn nhãn đáp án. Kết quả review thủ công dùng schema riêng. Schema này hỗ trợ nhiều reviewer và báo average, blocker rate, cùng số case chưa review. Khi chưa có thiết kế và dữ liệu phù hợp, runner không tính agreement.

## Documentation generation

`generate_docs.py` tạo tài liệu đọc nhanh từ YAML, gồm taxonomy, phạm vi, aggregation, severity, confidence, false-positive risk, rewrite strategy và exceptions. Chế độ `--check` ngăn tài liệu lệch catalog.

## Luồng thay đổi dữ liệu

Contributor sửa schema hoặc dữ liệu, thêm test, sinh docs, chạy validator, rồi nhờ reviewer bản ngữ kiểm phần rewrite. Một thay đổi chỉ đạt khi output chứng minh được từ input và context. Câu văn trôi chảy hơn không đủ.
