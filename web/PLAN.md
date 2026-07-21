# Kế hoạch: Web app "Vietnamese Writing Skills"

Tài liệu này mô tả kiến trúc và phạm vi cho phần web (`web/`) trong monorepo `vietnamese-humanizer`. Mục tiêu: một trang web để *kiểm tra* (check) và *gợi ý sửa* văn phong tiếng Việt, dựa trên chính package, patterns và skills của repo — nhưng **không** làm ảnh hưởng tới mục đích gốc (bộ Agent Skills + linter deterministic + corpus/benchmark có review).

## Nguyên tắc bất di bất dịch (đọc trước khi code)

Các nguyên tắc này bắt nguồn từ `README.md`, `docs/architecture.md`, `ROADMAP.md`. Vi phạm là làm hỏng mục đích repo:

1. **Không phân loại tác giả, không AI-probability score, không claim "vượt detector".** UI tuyệt đối không hiển thị kiểu "X% do AI viết".
2. **Linter chỉ nêu tín hiệu bề mặt để con người review.** `finding_type` (`error/warning/preference/heuristic`) là tín hiệu, không phải phán quyết "văn bản sai".
3. **Phần "check" là deterministic; phần "sửa" là generative và luôn phải được đánh dấu là gợi ý cần review.** Không trình bày bản rewrite như kết quả cuối chắc chắn đúng.
4. **Web chỉ TIÊU THỤ package, không sửa nó.** Không chỉnh `src/`, `patterns/`, `skills/`, `examples/`, `benchmarks/`, `tests/`. Không import source path trực tiếp — chỉ import package đã cài (`vietnamese_writing_skills`).
5. **Không tự động ghi dữ liệu người dùng vào `examples/examples.jsonl` hay `benchmarks/`.** Đóng góp corpus là quy trình PR riêng theo `CONTRIBUTING.vi.md` (xin phép, bỏ PII, review bản ngữ).
6. **Test của web là bộ test riêng.** Không trộn vào `pytest`/`tests/` gốc; CI Python hiện tại (`.github/workflows/ci.yml`) phải giữ nguyên hành vi.

## Cấu trúc monorepo

```
vietnamese-humanizer/            (repo gốc, GIỮ NGUYÊN)
├── src/ patterns/ skills/ examples/ benchmarks/ tests/ docs/ scripts/
├── pyproject.toml               (package Python gốc)
├── .github/workflows/ci.yml     (CI Python gốc — không đổi hành vi)
└── web/                         (MỚI — toàn bộ phần web nằm ở đây)
    ├── PLAN.md                  (tài liệu này)
    ├── GEMINI_PROMPT.md         (prompt để Gemini thực thi)
    ├── README.md                (hướng dẫn chạy web)
    ├── backend/                 (FastAPI, deploy Render)
    │   ├── app/
    │   │   ├── main.py          (khởi tạo FastAPI, CORS, router)
    │   │   ├── config.py        (đọc env: CORS origins, Gemini key, rate limit)
    │   │   ├── schemas.py       (Pydantic request/response models)
    │   │   ├── routers/
    │   │   │   ├── lint.py      (POST /api/lint — deterministic, bắt lỗi)
    │   │   │   ├── rewrite.py   (POST /api/rewrite — generative, Gemini viết lại)
    │   │   │   ├── patterns.py  (GET /api/patterns, /api/skills — metadata)
    │   │   │   ├── contributions.py (POST /api/contributions — user gửi case)
    │   │   │   ├── admin.py     (GET/PATCH /api/admin/contributions — duyệt, cần auth)
    │   │   │   └── health.py    (GET /api/health)
    │   │   ├── db/
    │   │   │   ├── database.py  (SQLAlchemy engine + session, đọc DATABASE_URL)
    │   │   │   └── models.py    (bảng Contribution)
    │   │   ├── limiter.py       (slowapi Limiter dùng chung)
    │   │   └── services/
    │   │       ├── linter.py    (wrap lint_text/pattern_index từ package)
    │   │       ├── rewriter.py  (gọi Gemini API với issue + SKILL.md context)
    │   │       └── contributions.py (CRUD staging case, export approved)
    │   ├── migrations/          (alembic; hoặc create_all lúc startup nếu đơn giản)
    │   ├── tests/               (pytest riêng cho backend)
    │   ├── pyproject.toml       (deps: fastapi, uvicorn, vietnamese-writing-skills, slowapi, sqlalchemy, ...)
    │   ├── requirements.txt     (hoặc dùng pyproject; cho Render)
    │   ├── render.yaml          (blueprint deploy Render + Postgres)
    │   └── .env.example
    └── frontend/                (Next.js App Router, deploy Vercel)
        ├── app/
        │   ├── page.tsx         (trang chính: editor + kết quả)
        │   ├── layout.tsx
        │   └── api/             (chỉ nếu cần proxy; ưu tiên gọi thẳng backend)
        ├── components/
        │   ├── Editor.tsx       (textarea/rich input)
        │   ├── IssueList.tsx    (danh sách phát hiện + severity badge)
        │   ├── IssueCard.tsx
        │   ├── RewritePanel.tsx (diff gốc vs gợi ý Gemini + nhãn cần review)
        │   ├── ContributeForm.tsx (form user gửi case + suggestion)
        │   └── Disclaimer.tsx   (banner: không phải AI-detector)
        ├── lib/
        │   ├── api.ts           (fetch client tới backend)
        │   └── types.ts         (mirror schema backend)
        ├── package.json
        ├── next.config.js
        ├── .env.local.example   (NEXT_PUBLIC_API_BASE_URL)
        └── vercel.json          (nếu cần)
```

## Backend — hợp đồng API

Backend là lớp mỏng bọc quanh package. **Không fork logic**, chỉ import và expose qua HTTP.

### Phụ thuộc vào package gốc

- Cài `vietnamese-writing-skills` như dependency (pin `==0.2.0` để ổn định; dev có thể `pip install -e ../..`).
- Import public API:
  - `from vietnamese_writing_skills.cli.lint import lint_text` — trả `list[dict]` mỗi issue có: `pattern_id, finding_type, severity, confidence, scope, line, column, excerpt, message, suggestion`.
  - `from vietnamese_writing_skills.core.patterns import pattern_index, iter_patterns` — metadata pattern.
  - `from vietnamese_writing_skills import __version__`.
- **Lưu ý về `data_location`** (`core/paths.py`): nó tự tìm repo root qua các marker `pyproject.toml/patterns/skills`. Trong monorepo dev, chạy backend từ `web/backend/` có thể khiến nó đi ngược lên tìm thấy repo gốc và dùng `patterns/` của repo — điều này OK cho dev. Trên Render (chỉ deploy code + cài package từ PyPI), nó sẽ dùng resource đóng gói trong wheel qua `importlib.resources`. Để tránh mơ hồ, service `linter.py` nên cho phép truyền `pattern_dir` tường minh nếu cần, mặc định để `None` (auto).

### `POST /api/lint` (deterministic — chức năng chính, an toàn)

Request:
```json
{
  "text": "Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới...",
  "skills": ["humanizer-vi", "style-guide-vi"]   // optional; null = tất cả
}
```

Response (bọc lại kết quả `lint_text` + summary giống `lint_file`):
```json
{
  "version": "0.2.0",
  "summary": {
    "total": 3,
    "error": 0, "warning": 1, "preference": 0, "heuristic": 2,
    "note": "Số phát hiện cần review, không phải xác suất văn bản do AI tạo."
  },
  "issues": [
    {
      "pattern_id": "VI-HUM-L02",
      "finding_type": "heuristic",
      "severity": "low",
      "confidence": "medium",
      "scope": "paragraph",
      "line": 1, "column": 1,
      "excerpt": "Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới.",
      "message": "...",
      "suggestion": "..."
    }
  ]
}
```

- Validate: `text` không rỗng, giới hạn độ dài (ví dụ 20.000 ký tự) để tránh abuse.
- `skills` chỉ nhận giá trị trong tập hợp lệ: `humanizer-vi, translationese-cleaner-vi, grammar-checker-vi, style-guide-vi`.
- Không lưu text người dùng (privacy). Có thể log ẩn danh số lượng issue nếu cần metric.
- **Rate limit:** 30 requests/phút/IP (slowapi) — đủ cho người dùng thật, chặn abuse.

### `GET /api/patterns` và `GET /api/skills`

- `/api/patterns`: trả metadata rút gọn từ `pattern_index()` (id, name, skill, finding_type, severity, summary) để frontend hiển thị mô tả khi user bấm vào một issue. **Không** trả toàn bộ YAML nặng.
- `/api/skills`: trả 4 skill với `name`, mô tả ngắn "dùng khi / không dùng khi" (lấy từ bảng trong README).
- **Rate limit:** 60 req/phút/IP (metadata nhẹ).

### `POST /api/rewrite` (generative — gọi Gemini, có chi phí)

Đây là phần *agent* nhờ Gemini viết lại văn bản, không phải linter. Trong khi `/api/lint` chỉ *bắt lỗi* (chỉ ra vị trí + tín hiệu), `/api/rewrite` *sinh bản viết lại* dựa trên các issue đó cộng hướng dẫn của skill.

Request:
```json
{
  "text": "...",
  "skill": "humanizer-vi",
  "issue_ids": ["VI-HUM-L02"]   // optional: chỉ tập trung vào các issue đã match
}
```

Luồng xử lý trong `rewriter.py`:
1. Chạy `lint_text` để lấy issue thật.
2. Đọc nội dung `SKILL.md` tương ứng qua helper package: `from vietnamese_writing_skills.core.paths import data_location` → `data_location('skills') / skill / 'SKILL.md'` (xử lý được cả source checkout lẫn wheel; KHÔNG hardcode `data/skills/...`). Lấy `rewrite_strategy` của các pattern liên quan từ `pattern_index()`.
3. Gọi Gemini API (SDK mới `google-genai`, model `gemini-2.0-flash` hoặc mới hơn) với system prompt ép **bảo toàn dữ kiện**: giữ nguyên số liệu, tên riêng, mức độ chắc chắn, register; không thêm ví dụ/nguồn/metric mới (giống ràng buộc `must_not_add` trong corpus).
4. Trả về `{ "rewrite": "...", "review_status": "unreviewed", "disclaimer": "Gợi ý do model sinh, cần người đọc kiểm chứng bảo toàn dữ kiện." }`.

Response BẮT BUỘC gắn `review_status: "unreviewed"` và disclaimer. Frontend hiển thị bản gốc và bản gợi ý cạnh nhau (diff), không tự động thay thế.

Cần `GEMINI_API_KEY` trong env. Nếu key vắng → endpoint trả 503 với thông báo rõ, phần `/api/lint` vẫn hoạt động bình thường.

- **Rate limit:** 5 req/phút/IP (chặt, vì tốn token Gemini).

## Đóng góp case (contribution) + Database

Người dùng có thể gửi case đề xuất (input + suggestion) để maintainer duyệt. **Đây là vùng staging, KHÔNG phải corpus.** DB chỉ lưu đề xuất; corpus gốc (`examples/examples.jsonl`) chỉ được cập nhật bằng tay qua PR theo `CONTRIBUTING.vi.md`.

### Vì sao tách DB khỏi corpus (nguyên tắc)

`CONTRIBUTING.vi.md` yêu cầu mỗi example phải: bỏ PII, có `context` đủ để kiểm chứng, `must_preserve`/`must_not_add`, pattern ID hợp lệ, và `preservation_review` provenance đúng. Không thể đảm bảo các ràng buộc này nếu tự động ghi input người dùng vào corpus. Nên: web nhận đề xuất → bạn duyệt trong DB → export case `approved` → tự tay chuẩn hóa + làm PR. Web KHÔNG bao giờ ghi trực tiếp vào `examples/` hay `benchmarks/`.

### Bảng `contributions` (SQLAlchemy)

| Cột | Kiểu | Ghi chú |
| --- | --- | --- |
| `id` | UUID/int PK | |
| `created_at` | datetime | |
| `input_text` | text | văn bản gốc user gửi |
| `context` | text | ngữ cảnh (optional, khuyến khích) |
| `suggestion` | text | bản sửa đề xuất của user |
| `skill` | text | 1 trong 4 skill hợp lệ |
| `pattern_ids` | text/JSON | pattern user cho là liên quan (optional) |
| `note` | text | ghi chú của user |
| `consent` | bool | user xác nhận không PII + có quyền chia sẻ (bắt buộc true) |
| `status` | enum | `pending` / `approved` / `rejected` (mặc định `pending`) |
| `review_note` | text | ghi chú của maintainer khi duyệt |
| `reviewed_at` | datetime | |

### `POST /api/contributions` (public, rate-limit mạnh)

Request:
```json
{
  "input_text": "...",
  "context": "...",
  "suggestion": "...",
  "skill": "humanizer-vi",
  "pattern_ids": ["VI-HUM-L02"],
  "note": "...",
  "consent": true
}
```
- Validate: `consent` phải `true` (nếu không → 400); `skill` trong tập hợp lệ; giới hạn độ dài từng field.
- Lưu vào DB với `status="pending"`.
- Trả `{ "id": "...", "status": "pending", "message": "Cảm ơn đóng góp, sẽ được maintainer xem xét." }`.
- **Rate limit:** 3 req/phút/IP + có thể thêm 20 req/ngày/IP để chống spam.
- KHÔNG hiển thị lại nội dung đóng góp của người khác cho công khai (tránh lạm dụng làm nơi đăng nội dung tùy ý).

### Admin (cần auth) — duyệt case

Bảo vệ bằng header `X-Admin-Key` khớp env `ADMIN_API_KEY`. Nếu sai/thiếu → 401.

- `GET /api/admin/contributions?status=pending` — liệt kê để duyệt.
- `PATCH /api/admin/contributions/{id}` — body `{ "status": "approved"|"rejected", "review_note": "..." }`.
- `GET /api/admin/contributions/export?status=approved` — xuất JSON các case đã duyệt để bạn dùng làm nguyên liệu PR corpus (KHÔNG tự ghi vào file repo).

### Database provisioning

- Dùng **Postgres trên Render** (free tier) qua `DATABASE_URL`. Dev local dùng SQLite (`sqlite:///./dev.db`) để không cần Postgres.
- Schema tạo bằng `Base.metadata.create_all()` lúc startup (đơn giản) hoặc Alembic nếu muốn migration bài bản.
- `render.yaml` khai báo cả web service lẫn Postgres database.

### Bảo mật & vận hành backend

- **CORS**: chỉ allow origin của frontend Vercel (đọc từ env `FRONTEND_ORIGIN`), không dùng `*` ở production.
- **Rate limit toàn bộ endpoint** bằng slowapi, áp dụng NGAY từ đầu: lint 30/phút, patterns/skills 60/phút, rewrite 5/phút, contributions 3/phút (+20/ngày). Key theo IP (`get_remote_address`), chú ý cấu hình đọc IP thật sau proxy Render (`X-Forwarded-For`).
- `/api/lint`, `/api/patterns`, `/api/skills`, `/api/contributions` là public (không auth) — ghi rõ trong README. `/api/admin/*` bắt buộc `ADMIN_API_KEY`.
- Không đọc/ghi file người dùng lên đĩa server. Text lint không lưu; chỉ contribution (khi user chủ động gửi) mới vào DB.

## Frontend — phạm vi

- Next.js (App Router) + TypeScript + Tailwind. Deploy Vercel.
- **Trang chính** (`/`): ô nhập văn bản, chọn skill (checkbox 4 skill), nút "Kiểm tra".
- **Kết quả:** danh sách issue nhóm theo `finding_type`, badge màu theo `severity`, hiển thị `line:column`, `excerpt`, `message`, `suggestion`. Bấm vào issue mở panel mô tả pattern (gọi `/api/patterns`).
- **Disclaimer cố định** (component `Disclaimer.tsx`): nêu rõ đây là công cụ nêu tín hiệu văn phong, KHÔNG phải AI-detector, không chấm điểm xác suất AI. Lấy tinh thần từ `README` đoạn "Dự án không phân loại tác giả...".
- **Nút "Gợi ý viết lại"** (component `RewritePanel.tsx`): gọi `/api/rewrite`, hiển thị diff gốc vs gợi ý Gemini, gắn nhãn "gợi ý cần review" rõ ràng. Không tự động thay thế.
- **Nút/trang "Đóng góp case"** (component `ContributeForm.tsx`): form nhập input + context + suggestion + skill + note, checkbox xác nhận PII + quyền chia sẻ (bắt buộc tick), gọi `POST /api/contributions`. Hiển thị thông báo thành công/lỗi. KHÔNG cho xem đóng góp của người khác (tránh lạm dụng).
- `NEXT_PUBLIC_API_BASE_URL` trỏ tới backend Render.
- i18n: mặc định tiếng Việt (đối tượng người dùng là người viết tiếng Việt).

## Deploy

### Backend → Render
- `web/backend/render.yaml` blueprint: web service Python + Postgres database, build `pip install -r requirements.txt` (hoặc `pip install .`), start `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- Env vars trên Render: `FRONTEND_ORIGIN`, `GEMINI_API_KEY`, `ADMIN_API_KEY`, `LINT_MAX_CHARS`, `DATABASE_URL` (Render tự inject từ database).
- Root directory của service = `web/backend` (Render hỗ trợ set root cho monorepo).
- `render.yaml` khai báo `databases:` (Postgres free) và link `DATABASE_URL` vào web service qua `fromDatabase`.

### Frontend → Vercel
- Project Root Directory = `web/frontend` (Vercel hỗ trợ monorepo qua Root Directory setting).
- Env: `NEXT_PUBLIC_API_BASE_URL` = URL Render backend.
- Build mặc định Next.js.

### CI cho web (tách khỏi CI Python gốc)
- Thêm workflow MỚI `.github/workflows/web-ci.yml` với `paths:` chỉ trigger khi `web/**` đổi. **Không sửa** `ci.yml` hiện có.
- Job backend: `pip install` trong `web/backend`, chạy `ruff`/`pytest` của backend.
- Job frontend: `npm ci` + `npm run build` + `npm run lint` trong `web/frontend`.

## Điều KHÔNG làm (ranh giới rõ ràng)

- Không sửa bất kỳ file nào ngoài `web/`, trừ: thêm `web-ci.yml` mới và (đã làm sẵn) cập nhật `.gitignore`.
- Không đổi `pyproject.toml` gốc, không đổi version package, không đụng `patterns/skills/examples/benchmarks/tests`.
- Không thêm dependency vào package gốc.
- Không tạo tính năng chấm điểm AI, không lưu trữ văn bản lint của người dùng.
- **Không tự động ghi contribution vào `examples/examples.jsonl` hay `benchmarks/`.** DB chỉ là staging; corpus cập nhật bằng tay qua PR.

## Tiêu chí hoàn thành (để verify)

1. `web/backend` chạy local: `uvicorn app.main:app` → `GET /api/health` trả version; `POST /api/lint` với văn bản mẫu trả issue khớp với `viet-writing-lint` CLI trên cùng văn bản.
2. `POST /api/rewrite` trả bản viết lại + `review_status: "unreviewed"` (mock Gemini trong test để không tốn token/không cần key).
3. `POST /api/contributions` lưu vào DB với `status="pending"`; từ chối khi `consent != true`. `/api/admin/*` trả 401 khi thiếu `ADMIN_API_KEY`, duyệt được khi đúng key.
4. Rate limit hoạt động: vượt ngưỡng trả 429.
5. `pytest` trong `web/backend/tests` xanh (dùng SQLite tạm cho test); không ảnh hưởng `pytest` gốc ở root.
6. `web/frontend` build được (`npm run build`), gọi được backend local, hiển thị issue + disclaimer + form đóng góp.
7. `ruff check .` và `pytest` ở ROOT vẫn xanh y như trước (không regression).
8. `git status` cho thấy mọi thay đổi nằm trong `web/`, `.gitignore`, và `.github/workflows/web-ci.yml`.
9. Không có file nào trong `src/ patterns/ skills/ examples/ benchmarks/ tests/` bị sửa.
</content>
</invoke>
