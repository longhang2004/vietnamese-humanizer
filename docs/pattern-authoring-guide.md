# Hướng dẫn viết pattern

## Một pattern đủ điều kiện merge

Một pattern phải có:

- lý do mô tả tác động lên người đọc, không chỉ nói “nghe như AI”;
- `finding_type`, `scope` và `aggregation` đúng với cách phát hiện;
- ít nhất hai ví dụ xấu từ ngữ cảnh khác nhau;
- ít nhất hai ví dụ tốt không thêm dữ kiện so với ví dụ nguồn;
- ngoại lệ, false-positive risk, severity và confidence;
- tín hiệu đủ hẹp hoặc mô tả rõ vì sao chỉ reviewer xử lý được;
- test hoặc benchmark case;
- kiểm tra không trùng pattern hiện có.

## Chọn finding type

- `error`: lỗi có thể chứng minh tương đối rõ trong convention đã chọn.
- `warning`: có khả năng gây mơ hồ hoặc không nhất quán nhưng cần ngữ cảnh.
- `preference`: lựa chọn phong cách, không được gọi là lỗi.
- `heuristic`: tín hiệu bề mặt cần reviewer đọc toàn phạm vi.

Không nâng một preference thành error chỉ vì maintainer thích một cách viết.

## Chọn scope và aggregation

`scope` là đơn vị tối thiểu cần đọc: token, phrase, sentence, paragraph hoặc document. `aggregation` mô tả cách nhiều quan sát tạo thành finding: single, count, density, sequence, variance hoặc consistency.

Phrase dịch sát thường dùng `phrase/single`. Lặp mở đầu câu dùng `paragraph/sequence`; mật độ từ nối dùng `paragraph/density`; nhịp câu dùng `document/variance`; trộn đại từ dùng `document/consistency`.

## Severity, confidence và false positive

Severity đo tác hại nếu finding đúng trong ngữ cảnh. Confidence đo độ chắc của tín hiệu. False-positive risk ghi khả năng rule chạm trường hợp hợp lệ. Ba trường này có vai trò khác nhau.

## Viết signals

Phrase và regex phải đủ hẹp. Với pattern theo mật độ hoặc count, đặt `min_occurrences` phù hợp. Kiểm regex trên ví dụ hợp lệ, code, URL và thuật ngữ ngành. CLI che một số vùng, nhưng pattern vẫn phải tự giới hạn.

## Ví dụ và preservation

Ví dụ tốt chỉ dùng thông tin có trong câu nguồn hoặc context được lưu rõ. Không thay “cải thiện hiệu suất” bằng một metric tự chọn. Không thêm deadline, nguyên nhân, nguồn, trải nghiệm hay cơ chế kỹ thuật.

Mỗi `good_examples` phải có `mode`: `clean_rewrite`, `review_comment`, `needs_author_decision` hoặc `no_change`. Review comment không phải câu thay thế. Nếu không thể sửa an toàn vì thiếu nguồn hoặc có nhiều cách hiểu, không gắn lời bình meta nhãn `clean_rewrite`.

Trước khi chấp nhận một good example, reviewer xác nhận:

- [ ] Giữ mệnh đề chính, chủ thể, đối tượng và phạm vi.
- [ ] Giữ số lượng, thời gian, quan hệ nhân quả, điều kiện và ngoại lệ.
- [ ] Giữ mức độ bắt buộc, mức độ chắc chắn và lập trường.
- [ ] Không thêm metric, nguồn, tác nhân, cơ chế, nguyên nhân hoặc kết quả.
- [ ] Mọi dữ kiện ngoài input đều có trong `context`.
- [ ] Không đổi ngôi xưng hoặc register ngoài phạm vi pattern.
- [ ] Chỉ sửa tín hiệu mà pattern nhắm tới.
- [ ] Nếu không thể clean rewrite, dùng `review_comment` hoặc `needs_author_decision`.

Example corpus dùng `examples/schema.json`. Một example mới cần input, context, output, output mode, must-preserve, must-not-add, gold metadata và preservation review có provenance. Dùng `unreviewed` nếu chưa audit. Trạng thái đó không được là gold rewrite.

Ưu tiên ví dụ tự viết hoặc đã được phép dùng. Nếu lấy từ quan sát thực tế, ẩn chi tiết nhận dạng và kiểm license.

## Checklist lệnh

```bash
python scripts/generate_pattern_docs.py
python scripts/validate_patterns.py
python scripts/validate_examples.py
pytest
python scripts/run_benchmarks.py --validate-only
```
