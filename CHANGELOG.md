# Changelog

Tuân theo Keep a Changelog ở mức cấu trúc, chưa cam kết Semantic Versioning trước bản 1.0.

## [Unreleased]

Chưa có thay đổi.

## [0.2.0] - 2026-07-20

### Added

- JSON Schema và validator cho 100 example đã agent-audit preservation, gồm output mode, gold rewrite/classification và review provenance.
- Finding taxonomy, scope và aggregation cho toàn bộ 40 pattern.
- Pattern example modes và generated docs hiển thị mode của từng good example.
- Expected output mode, manual review schema, blocker rate, multi-reviewer summary và unreviewed count cho benchmark.
- Package `vietnamese_writing_skills`, sáu console commands và wheel resources.
- Python 3.11, 3.12 và 3.13 CI matrix cùng wheel smoke test.

### Changed

- Hoàn tất semantic preservation audit; loại bỏ context ẩn và không tự chọn chủ thể, phạm vi hoặc năm còn mơ hồ.
- Linter xuất error, warning, preference và heuristic cùng confidence, scope và summary theo loại.
- `scripts/` chỉ còn wrapper tương thích; logic importable chuyển vào `src/`.
- README dùng repository URL thật và giải thích repository, product, distribution và import name.
- Generated docs hiển thị đầy đủ taxonomy, strategy, exceptions và false-positive risk.

## [0.1.0] - 2026-07-20

MVP đầu tiên sẵn sàng cho review công khai.
