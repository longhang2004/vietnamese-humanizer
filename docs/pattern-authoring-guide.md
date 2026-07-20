# Hướng dẫn viết pattern

## Một pattern đủ điều kiện merge

Pattern phải có:

- lý do mô tả tác động lên người đọc, không chỉ nói "nghe như AI";
- ít nhất hai ví dụ xấu từ ngữ cảnh khác nhau;
- ít nhất hai cách sửa hoặc hai output tốt;
- ngoại lệ và phản biện trường hợp cấu trúc hợp lệ;
- domain, category, severity, confidence và false-positive risk;
- tín hiệu có thể kiểm tra hoặc mô tả rõ vì sao chỉ reviewer xử lý được;
- test hoặc benchmark case;
- kiểm tra không trùng pattern hiện có.

## Chọn severity và confidence

Severity đo tác hại nếu pattern xuất hiện trong ngữ cảnh bị nêu. High dành cho nguy cơ đổi nghĩa, nguồn hoặc trách nhiệm; medium cho độ rõ và register; low cho nhịp hoặc nhất quán ít ảnh hưởng.

Confidence đo độ chắc của tín hiệu, không phải mức nghiêm trọng. Regex dấu câu có thể high confidence. Nhịp câu đều thường low confidence.

## Viết signals

Phrase và regex phải đủ hẹp. Với pattern phong cách, đặt `min_occurrences` từ 2 trở lên trừ công thức đặc hiệu. Kiểm regex trên ví dụ hợp lệ, code, URL và thuật ngữ ngành. CLI che một số vùng nhưng pattern vẫn nên tự giới hạn.

## Ví dụ và quyền riêng tư

Ưu tiên ví dụ tự viết hoặc đã được phép dùng. Nếu lấy từ quan sát thực tế, ẩn tên, số tài khoản, địa chỉ và chi tiết nhận dạng. Không thay vài từ rồi coi đó là dữ liệu vô danh nếu người đọc vẫn nhận ra nguồn.

## Nguồn quan sát

Khuyến nghị ghi issue hoặc PR: nguồn quan sát, domain, vùng ngôn ngữ, thế hệ, register, số lần gặp, phản ví dụ và nhận xét của người bản ngữ. Không dùng một giọng miền làm chuẩn cho toàn bộ tiếng Việt.

## Checklist lệnh

```bash
python scripts/generate_pattern_docs.py
python scripts/validate_patterns.py
pytest
python scripts/run_benchmarks.py --validate-only
```
