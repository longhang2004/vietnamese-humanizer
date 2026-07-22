**Tiếng Việt** | [English](CHANGELOG.md)

# Nhật ký thay đổi (Changelog)

Tuân theo cấu trúc Keep a Changelog. Chưa cam kết Semantic Versioning trước bản 1.0.

## [Unreleased]

## [0.4.2] - 2026-07-22

### Added

- Bổ sung capability gate fail-closed cho rewrite, lưu contribution và admin; health endpoint trả thêm capability public đang có hiệu lực.
- Bổ sung workflow native `doctor`/`setup`/`demo`/`check`/`smoke` và mở rộng Web CI để bao phủ core cùng tài nguyên đóng gói.
- Bổ sung Code of Conduct, CODEOWNERS và hướng dẫn maintainer cho quy trình local/deploy an toàn.

### Changed

- Dùng metadata package gốc làm nguồn version runtime và đồng bộ dependency backend, OpenAPI, health, lint response cùng cấu hình deploy.
- Giao diện chỉ hiện tính năng tùy chọn khi backend bật capability; vẫn giữ Vercel Analytics nhưng không thêm custom event hoặc telemetry suy ra từ nội dung.
- Render blueprint bật contribution/admin một cách rõ ràng và đặt rewrite ở trạng thái tắt.
- Nâng frontend lên Next.js 16 và ESLint flat config, đồng thời pin các dependency gián tiếp xử lý ảnh/CSS đã vá để xử lý cảnh báo bảo mật production trước khi phát hành.

### Fixed

- Sửa production dependency còn pin ở `0.2.0` và thêm release-consistency gate.
- Bảo đảm route bị tắt trả `503` ổn định trước khi parse body, gọi provider, xác thực hoặc truy cập database.
- Không để chi tiết exception từ provider lộ ra client rewrite; so sánh admin key theo constant-time và an toàn với Unicode.

## [0.4.1] - 2026-07-22

### Added

- Hỗ trợ cài đặt bằng `npx skills add` và cập nhật hướng dẫn trong `README.md` & `README.vi.md`.
- Thêm các thư mục artifact khi cài skill cục bộ (`.agents/`, `.claude/`, `agent/`, `skills-lock.json`) vào `.gitignore`.

### Fixed

- Xử lý mượt mà trường hợp GitHub Release đã tồn tại trong Release CI workflow bằng `gh release upload --clobber`.

## [0.4.0] - 2026-07-22

### Added

- Tái thiết kế toàn bộ giao diện Web UI (Next.js Frontend) theo Anti-Slop (`taste-skill`) và Design System (`ui-ux-pro-max-skill`).
- Tích hợp font chữ hiện đại Google Fonts: `Plus Jakarta Sans` (sans-serif) và `JetBrains Mono` (monospace).
- Thêm bộ đếm ký tự/từ ngữ theo thời gian thực, nút xóa văn bản nhanh và nút nạp văn bản mẫu.
- Thẻ lựa chọn kỹ năng (Skill Cards) và danh sách phát hiện lỗi trực quan với thẻ phân loại độ nghiêm trọng, badge monospace và gợi ý diễn đạt lại.
- Modal xem chi tiết quy chuẩn gọt giũa kèm hiệu ứng mờ nền `backdrop-blur-sm`.
- Chuẩn hóa toàn bộ câu chữ và nhãn giao diện (UI Copy & Microcopy) theo đúng quy chuẩn diễn đạt tự nhiên của `vietnamese-writing-skills`.

### Fixed

- Truyền repository context rõ ràng cho bước tạo GitHub Release khi job không checkout source.

### Changed

- Biên tập lại tài liệu công khai bằng giọng văn tự nhiên, trực tiếp hơn.

## [0.3.1] - 2026-07-22

### Added

- Tích hợp Vercel Analytics (`@vercel/analytics`) theo dõi lượng truy cập web app.
- Cập nhật PyPI release workflow hỗ trợ `skip-existing: true` chống lỗi 400 khi file đã tồn tại trên PyPI.

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
