**Tiếng Việt** | [English](CHANGELOG.md)

# Nhật ký thay đổi (Changelog)

Tuân theo cấu trúc Keep a Changelog. Chưa cam kết Semantic Versioning trước bản 1.0.

## [Unreleased]

### Added

- Landing page tối, công cụ riêng tại `/check`, trang ví dụ, hướng dẫn và giới thiệu dự án; số sao lấy từ GitHub, font tiếng Việt tự host và điều hướng responsive. Áp dụng UI/UX Pro Max và Impeccable cho thiết kế.
- Sáu cặp biên tập thật bằng Codex subagent, cùng yêu cầu, giữ nguyên đầu ra và có bản ghi, hash nguồn, kiểm đồng bộ. Ví dụ nằm riêng khỏi corpus và benchmark; chưa có kết quả đo cải thiện chất lượng.

### Changed

- Rà và refactor UI tối bằng plugin Impeccable: thu gọn phần chọn nhóm kiểm tra, dùng chung control cho onboarding, tăng cỡ chữ lệnh cài và vùng bấm. Sửa lệch cột, cấp tiêu đề, thông báo cho trình đọc màn hình và đóng menu bằng Escape.

### Fixed

- Bổ sung driver Psycopg 3 dạng binary để backend nạp được cấu hình PostgreSQL hiện tại, giữ tương thích Psycopg 2. Có test cho driver chỉ định và URL PostgreSQL mới/cũ, không kết nối database thật.
- Trình soát bỏ kết quả hoặc lỗi trả về muộn khi nội dung hay nhóm kiểm tra đã đổi. Kết quả có đủ bốn nhóm lọc và phần giải thích quy tắc mở ngay tại chỗ.

## [0.6.0] - 2026-11-04

### Changed

- Bổ sung nguồn tiếng Việt và hướng dẫn rà khuôn lời chúc/tri ân, thông tin riêng của đối tượng và chức năng dấu câu; có ví dụ tự viết, đồng bộ lại bộ tải.
- Bổ sung hướng dẫn lối viết theo khuôn từ nghiên cứu và thảo luận năm 2026, có nguồn, phản ví dụ, nạp vào prompt viết lại và 12 benchmark tự viết. Giữ nguyên 44 pattern; chưa có điểm nguồn gốc hay kết quả đo cải thiện chất lượng.
- Thêm rule xét vai trò của định nghĩa, lời hướng dẫn, lưu ý và câu phủ định theo ngữ cảnh: giữ phần giúp người đọc làm việc hiện tại và các điều kiện có ý nghĩa, tránh tự biến mọi đoạn thành bài hướng dẫn. Áp dụng lên web và tách mô tả tác vụ cho người dùng khỏi mô tả kích hoạt dành cho AI.
- Dùng chính các skill biên tập tiếng Việt của dự án để sửa câu chữ trên web: hướng dẫn rõ và gần gũi, tên tác vụ nhất quán, trạng thái gợi ý dễ hiểu hơn và có quy ước viết cho giao diện. Sinh lại bộ tải từ catalog đã sửa.

### Added

- Thêm profile hành chính, bài đăng mạng xã hội và marketing, có nguồn đọc sơ cấp, reference riêng, lựa chọn trên API/web và 18 benchmark đối chiếu ngữ cảnh tự viết (tổng 124). Profile giữ các lựa chọn giọng/kênh/mức sửa; chưa có kết quả đánh giá độc lập bởi người bản ngữ.

- Trang `/start` cho người không viết code: chọn chatbot và nhu cầu, hướng dẫn cài theo nền tảng, sao chép yêu cầu hoặc tự sao chép khi clipboard bị chặn.
- Gói ZIP Claude/Gemini, gói plugin ChatGPT chuẩn bị nộp, tài liệu Markdown tự chứa và kiểm đồng bộ trong CI. Release đính kèm bộ tải riêng với gói Python; chưa có listing plugin công khai.
- Lựa chọn loại bài độc lập trong API và web rewrite: giữ nguyên, văn viết rõ ràng, trao đổi công việc và tài liệu kỹ thuật. Profile giữ lựa chọn kênh, giọng, xưng hô và mức sửa của người dùng.
- Reference tiếng Việt theo loại bài, ví dụ tự viết có chú giải và ghi nguồn đọc Google, Mailchimp, NN/g.
- Thêm 24 benchmark do agent tự viết theo 12 cặp, quy trình review bản ngữ và báo cáo theo profile/system. Chưa có điểm chất lượng độc lập.
- Danh mục nhóm văn phong có nguồn đọc, quy trình học cùng chủ đề và pilot bốn biến thể đã chạy bằng subagent, biên tập rồi review định tính bằng AI. Dữ liệu pilot nằm riêng khỏi corpus và baseline benchmark.

## [0.5.0] - 2026-10-31

### Added

- Hướng dẫn mạch thông tin, kết hợp từ, lược chủ ngữ, phép lặp và sắc thái; ghi nguồn đọc có tác giả; tách hướng dẫn chat và kịch bản nói.
- Rewrite nhận context và profile tùy chọn, nạp reference phù hợp, trả output mode để tách nhận xét khỏi văn bản thay thế.
- Thêm 30 benchmark dài do agent tự viết theo 15 cặp, nâng tổng số lên 70. Chưa có baseline được người thật đánh giá.

### Changed

- Rà lại sáu ví dụ corpus để tránh chỉ đổi từ đồng nghĩa, ghi rõ quyền giảm cường điệu và chuyển nhận định quảng cáo thiếu căn cứ sang góp ý.
- Client rewrite cần đọc `output_mode`: góp ý và câu hỏi cho tác giả trả `rewrite` rỗng cùng `comments`. Web đã xử lý cả bốn mode.

### Fixed

- Nâng Next.js và công cụ kiểm thử frontend lên nhánh đã vá, cập nhật dependency gián tiếp có lỗ hổng và giữ nguyên cổng kiểm tra audit trong CI.
- Audit không còn lỗi high/critical; vẫn có cảnh báo moderate của `minimatch` trong công cụ lint phục vụ phát triển.

## [0.4.6] - 2026-09-18

### Fixed

- Chỉ tin header proxy từ IP/CIDR trong allowlist, tự triển khai không dùng API nội bộ của uvicorn nên `uvicorn>=0.30.0` vẫn import được; duyệt `X-Forwarded-For` từ phải sang trái để nhiều proxy không gom quota của client.
- Linter: ngoặc kép cong, fence bốn backtick, và gom HUM-S01/S03 theo đoạn, kể cả mục list với HUM-S03.
- Giảm báo nhầm `vì vậy nên` khi là lời khuyên (chỉ cảnh báo khi có cụm chủ ngữ đầy đủ như `công ty`/`dữ liệu`/`cuộc họp` kèm vị ngữ kết quả; cụm động từ hoặc trường hợp chưa chắc được giữ nguyên), từ láy như “người người” và “từ từ”, email/tên tệp/viết tắt, `bạn` với `người dùng`, acronym đã giải thích, link Markdown, URL trong ngoặc kép ASCII/cong, URL có ngoặc đơn hoặc ngoặc IPv6, khoảng trắng Unicode sau URL, và ký hiệu đánh số.
- Panel viết lại không giữ kết quả của văn bản A sau khi lint văn bản B.
- CORS trên Render cho phép origin Vercel đang công bố.

### Changed

- Next.js 16.3.x (sharp/postcss đã vá); rewrite Gemini gửi đủ skill và fallback `gemini-2.5-flash-lite`.
- Catalog 44 pattern và 40 benchmark case, thêm fixture `no_change`.

## [0.4.5] - 2026-07-25

### Fixed

- Giảm false positive trong phát hiện viết tắt VI-STY-T02 bằng cách loại trừ từ tiếng Việt nhấn mạnh (NGAY, MUA, GIẢM...), viết tắt hành chính VN phổ biến (UBND, CSGT, BHXH, CMND, CCCD...), thuật ngữ tech bổ sung (APP, APK, WIFI...) và văn bản trong ngoặc kép.
- Bổ sung heuristic nhận biết ngữ cảnh để bỏ qua từ tiếng Việt viết hoa có dấu và cụm viết hoa trong ngữ cảnh CTA/quảng cáo.

### Changed

- Mở rộng exclude_phrases của VI-STY-T02 từ ~20 lên ~130+ entries bao gồm từ vựng tech, business, hành chính và nhấn mạnh.

## [0.4.4] - 2026-07-22

### Added

- Bổ sung contract test thực thi toàn bộ 43 rule, cùng example và benchmark cho cặp từ nối không khớp, từ nối kết quả bị chồng và lớp diễn đạt hành chính dày.
- Bổ sung regression coverage cho ranh giới câu, nội dung được bảo vệ, các kiểu aggregation, acronym đã giải thích và excerpt dài.

### Changed

- Cập nhật cả bốn skill tiếng Việt lên `0.2.1` với hướng dẫn ngắn gọn cho các rule đã sửa, trong khi catalog YAML vẫn là nguồn có thẩm quyền.
- Mở rộng corpus đã review lên 103 example và bộ benchmark lên 33 case.

### Fixed

- Không để pattern grammar và humanizer theo phạm vi câu match xuyên ranh giới câu; nhận thêm biến thể có dấu phẩy “vì vậy, nên”.
- Không cảnh báo acronym tại lần định nghĩa đầu tiên và giới hạn excerpt đúng 100 ký tự ngay cả khi match dài hơn.

## [0.4.3] - 2026-07-22

### Added

- Bổ sung kiểm tra có mục tiêu cho cặp quan hệ từ không khớp, cụm “vì vậy nên” thừa và mật độ lớp diễn đạt hành chính.
- Bổ sung danh sách vị trí vào lint finding để một finding đã gom vẫn giữ đủ mọi đoạn khớp.

### Changed

- Gom tín hiệu count, density và consistency theo finding cần review thay vì tạo một card cho mỗi raw match.
- Đặt excerpt quanh đoạn khớp và sửa empty state của web để mô tả đúng giới hạn bộ quy tắc.

### Fixed

- Không còn bắt danh từ chung viết thường bằng rule viết hoa; sửa consistency check cho đại từ, thuật ngữ và khoảng trắng phần trăm.
- Không để regex câu bị động nuốt qua nhiều mệnh đề.

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
