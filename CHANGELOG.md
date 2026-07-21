# Changelog

Tuân theo Keep a Changelog ở mức cấu trúc, chưa cam kết Semantic Versioning trước bản 1.0.

## [Unreleased]

### Fixed

- Truyền repository context rõ ràng cho bước tạo GitHub Release khi job không checkout source.

### Changed

- Biên tập lại tài liệu công khai bằng giọng văn tự nhiên, trực tiếp hơn.

## [0.3.0] - 2026-07-22

### Added

- Web Application "Vietnamese Writing Skills" (`web/`): bao gồm FastAPI Backend và Next.js Frontend.
- Tích hợp Gemini AI (`gemini-2.5-flash`) cho tính năng Gợi ý viết lại tự nhiên và bảo toàn dữ kiện.
- Cơ sở dữ liệu Staging (PostgreSQL / Neon) để lưu vết các case đóng góp từ cộng đồng.
- Tối ưu hóa SEO toàn diện (Detailed SEO Standard): OpenGraph banner, Twitter card, Favicon, JSON-LD Schema và Canonical metadata.
- Ghi nhận Contributor mới: **Lê Ngọc Phương Thư** (`lengocphuongthuct2006@gmail.com`) — Tác giả đề xuất và lên ý tưởng phiên bản Web App.

## [0.2.0] - 2026-07-21

### Added

- JSON Schema và validator cho 100 example đã agent-audit preservation, gồm output mode, gold rewrite/classification và review provenance.
- Finding taxonomy, scope và aggregation cho toàn bộ 40 pattern.
- Pattern example modes và generated docs hiển thị mode của từng good example.
- Expected output mode, manual review schema, blocker rate, multi-reviewer summary và unreviewed count cho benchmark.
- Package `vietnamese_writing_skills`, sáu console commands và wheel resources.
- Tài liệu công khai song ngữ Anh–Việt cho README và hướng dẫn đóng góp.
- Mục ủng hộ dự án bằng mã VietQR trong cả hai README.
- Workflow phát hành theo tag với artifact dùng chung, GitHub Release và PyPI Trusted Publishing qua OIDC.
- Chính sách báo cáo lỗ hổng và cấu hình Dependabot cho Python cùng GitHub Actions.
- Python 3.11–3.14 CI matrix, kiểm artifact bằng Twine và smoke test đủ sáu console command.

### Changed

- Hoàn tất semantic preservation audit; loại bỏ context ẩn và không tự chọn chủ thể, phạm vi hoặc năm còn mơ hồ.
- Linter xuất error, warning, preference và heuristic cùng confidence, scope và summary theo loại.
- `scripts/` chỉ còn wrapper tương thích; logic importable chuyển vào `src/`.
- README dùng repository URL thật và giải thích repository, product, distribution và import name.
- Generated docs hiển thị đầy đủ taxonomy, strategy, exceptions và false-positive risk.
- Bổ sung metadata package, project URLs và classifier Python 3.11–3.14.
- Chuyển các hạng mục 0.2 chưa hoàn tất trong roadmap sang nhóm 0.2.x / Post-0.2.

## [0.1.0] - 2026-07-20

MVP đầu tiên sẵn sàng cho review công khai.
