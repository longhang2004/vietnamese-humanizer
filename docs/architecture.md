# Kiến trúc

Repository có năm lớp tách biệt.

## Agent Skills layer

Bốn thư mục trong `skills/` chứa quy trình ra quyết định và kiến thức biên tập. `SKILL.md` ngắn, còn reference chỉ được nạp khi cần. Logic ngôn ngữ chính nằm ở đây vì sửa câu cần hiểu mục đích, độc giả, register, mơ hồ và dữ kiện mà regex không xử lý được.

## Pattern data layer

Các file YAML trong `patterns/` lưu phần pattern có thể kiểm tra, sinh tài liệu hoặc dùng làm gợi ý. JSON Schema giữ cấu trúc ổn định. YAML không phải từ điển lỗi; mỗi mục có ngoại lệ và rủi ro false positive.

## Deterministic validation layer

`validate_skills.py` kiểm frontmatter, tên, link và progressive disclosure. `validate_patterns.py` kiểm schema, ID, regex và generated docs. `lint_vietnamese.py` chỉ tìm tín hiệu bề mặt và bảo vệ code, URL, identifier. CLI không tự sửa trong MVP.

## Benchmark layer

Benchmark tách khỏi unit test. Unit test có đáp án đúng deterministic; biên tập ngôn ngữ thường có nhiều output tốt. Benchmark lưu input, ràng buộc, thành phần phải giữ và rubric cho reviewer.

## Documentation generation layer

`generate_pattern_docs.py` tạo một bảng đọc nhanh từ YAML. Chạy ở chế độ `--check` trong CI để ngăn tài liệu lệch catalog.

## Luồng thay đổi pattern

Contributor sửa YAML, thêm test hoặc benchmark, sinh docs, chạy validators, rồi nhờ reviewer bản ngữ đánh giá ví dụ và ngoại lệ. Không gộp mọi nội dung vào một `SKILL.md` vì agent sẽ phải nạp hàng nghìn dòng dù tác vụ chỉ cần một nhóm quy tắc.
