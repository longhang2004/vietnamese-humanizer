# Kiến trúc

Repository tách dữ liệu ngôn ngữ, logic deterministic và quy trình review. Mỗi lớp chỉ xử lý phần có thể kiểm chứng.

## Agent Skills

Bốn thư mục trong `skills/` chứa quy trình ra quyết định và kiến thức biên tập. `SKILL.md` giữ hướng dẫn cốt lõi; reference chỉ nạp khi cần. Agent hoặc reviewer thực hiện bản viết lại vì quyết định sửa cần xét mục đích, độc giả, register, thuật ngữ, chỗ mơ hồ và dữ kiện của toàn văn bản.

## Pattern data

Các file YAML trong `patterns/` lưu tín hiệu có thể kiểm tra hoặc gợi ý review. JSON Schema bắt buộc `finding_type`, `scope` và `aggregation`. Catalog không phải từ điển lỗi. Dù heuristic có regex ổn định, reviewer vẫn phải đánh giá tác động trong đoạn hoặc toàn tài liệu.

## Example corpus

`examples/examples.jsonl` lưu 100 cặp input/output. Mỗi dòng có `context`, `must_preserve`, `must_not_add` và `preservation_review`. Context tách khỏi input để reviewer biết output được phép dùng dữ kiện nào. Cách này tránh các giải thích mơ hồ như “chi tiết đã có trong bài”. JSON Schema kiểm cấu trúc và tham chiếu pattern, không tự chứng minh bảo toàn ngữ nghĩa.

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

Benchmark tách khỏi unit test. Case lưu input, context, constraints, must-preserve, must-not-add và blocker. Kết quả review thủ công dùng schema riêng. Schema này hỗ trợ nhiều reviewer và báo average, blocker rate, cùng số case chưa review. Khi chưa có thiết kế và dữ liệu phù hợp, runner không tính agreement.

## Documentation generation

`generate_docs.py` tạo tài liệu đọc nhanh từ YAML, gồm taxonomy, phạm vi, aggregation, severity, confidence, false-positive risk, rewrite strategy và exceptions. Chế độ `--check` ngăn tài liệu lệch catalog.

## Luồng thay đổi dữ liệu

Contributor sửa schema hoặc dữ liệu, thêm test, sinh docs, chạy validator, rồi nhờ reviewer bản ngữ kiểm phần rewrite. Một thay đổi chỉ đạt khi output chứng minh được từ input và context. Câu văn trôi chảy hơn không đủ.
