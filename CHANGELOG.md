# Changelog

Tuân theo Keep a Changelog ở mức cấu trúc, chưa cam kết Semantic Versioning trước bản 1.0.

## [Unreleased]

### Added

- JSON Schema và validator cho 100 example đã audit preservation.
- Finding taxonomy, scope và aggregation cho toàn bộ 40 pattern.
- Manual review schema, blocker rate, multi-reviewer summary và unreviewed count cho benchmark.
- Package `vietnamese_writing_skills`, sáu console commands và wheel resources.
- Python 3.11, 3.12 và 3.13 CI matrix cùng wheel smoke test.

### Changed

- Loại bỏ context ẩn khỏi example và pattern rewrite; mọi dữ kiện ngoài input được lưu trong context.
- Linter xuất error, warning, preference và heuristic cùng confidence, scope và summary theo loại.
- `scripts/` chỉ còn wrapper tương thích; logic importable chuyển vào `src/`.
- README dùng repository URL thật và giải thích repository, product, distribution và import name.
- Generated docs hiển thị đầy đủ taxonomy, strategy, exceptions và false-positive risk.

## [0.1.0] - 2026-07-20

MVP đầu tiên sẵn sàng cho review công khai.
