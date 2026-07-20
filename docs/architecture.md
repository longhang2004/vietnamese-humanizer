# Kiến trúc

Repository tách dữ liệu ngôn ngữ, logic deterministic và quy trình review để mỗi lớp chỉ chịu trách nhiệm cho điều nó có thể kiểm chứng.

## Agent Skills

Bốn thư mục trong `skills/` chứa quy trình ra quyết định và kiến thức biên tập. `SKILL.md` giữ phần hướng dẫn cốt lõi; reference chỉ được nạp khi cần. Rewrite nằm ở agent hoặc reviewer vì quyết định sửa phụ thuộc mục đích, độc giả, register, thuật ngữ, mơ hồ và dữ kiện của toàn văn bản.

## Pattern data

Các file YAML trong `patterns/` lưu tín hiệu có thể kiểm tra hoặc dùng làm gợi ý. JSON Schema bắt buộc `finding_type`, `scope` và `aggregation`. Catalog không phải từ điển lỗi. Một heuristic có thể có regex ổn định nhưng vẫn cần reviewer đánh giá tác động trong cả đoạn hoặc tài liệu.

## Example corpus

`examples/examples.jsonl` lưu 100 cặp input/output. Mỗi dòng có `context`, `must_preserve`, `must_not_add` và `preservation_review`. Tách context khỏi input giúp reviewer biết output được phép dùng dữ kiện nào, đồng thời loại bỏ lời giải thích mơ hồ như “chi tiết đã có trong bài”. JSON Schema kiểm cấu trúc và tham chiếu pattern, nhưng không tự chứng minh bảo toàn ngữ nghĩa.

## Python package

Logic importable nằm dưới `src/vietnamese_writing_skills/`:

- `core/` đọc resource, kiểm frontmatter, pattern, example và benchmark;
- `cli/` chứa linter, validator, benchmark runner và generator;
- `data/` là namespace cho resource được đưa vào wheel.

Các file trong `scripts/` không phải package Python. Chúng chỉ gọi `main()` từ package chính thức để giữ tương thích với command cũ.

## Package resources

Hatch đưa `patterns/`, `skills/`, `examples/` và `benchmarks/` vào `vietnamese_writing_skills/data/` trong wheel. Khi CLI chạy trong source checkout, nó dùng dữ liệu của repository để maintainer thấy thay đổi đang sửa. Khi chạy ngoài checkout, lệnh đọc dữ liệu dùng `importlib.resources`. Option `--root PATH` cho phép kiểm một repository bất kỳ.

Wheel phải chứa resource vì linter và validator cần schema/YAML sau khi cài ở một môi trường khác. Chỉ đóng gói Python module sẽ làm command chạy được `--help` nhưng lỗi ngay khi xử lý văn bản.

## Deterministic validation và linter

Validator kiểm schema, ID trùng, regex, link, review status và generated docs. Linter che fenced code, inline code, URL và một số identifier rồi phát hiện tín hiệu bề mặt. Output phân biệt error, warning, preference và heuristic; không có AI score.

Regex không đủ để humanize. Nó không biết một metric có tồn tại trong nguồn, đại từ nào phù hợp quan hệ xã hội, hay bị động có cần trong phương pháp nghiên cứu. Vì vậy CLI chỉ nêu vị trí và đề xuất review, không tự rewrite.

## Benchmark

Benchmark tách khỏi unit test. Case lưu input, context, constraints, must-preserve, must-not-add và blocker. Kết quả review thủ công dùng schema riêng, hỗ trợ nhiều reviewer, báo average, blocker rate và số case chưa review. Runner không tính agreement giả khi chưa có thiết kế và dữ liệu phù hợp.

## Documentation generation

`generate_docs.py` tạo tài liệu đọc nhanh từ YAML, gồm taxonomy, phạm vi, aggregation, severity, confidence, false-positive risk, rewrite strategy và exceptions. Chế độ `--check` ngăn tài liệu lệch catalog.

## Luồng thay đổi dữ liệu

Contributor sửa schema hoặc dữ liệu, thêm test, sinh docs, chạy validator rồi nhờ reviewer bản ngữ kiểm phần rewrite. Một thay đổi chỉ đạt khi output có thể được chứng minh từ input và context, không phải khi câu mới nghe trôi chảy hơn.
