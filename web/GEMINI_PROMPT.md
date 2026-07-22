# Prompt cho Gemini: Thực thi Web App

> **Tài liệu lịch sử (historical):** Prompt này ghi lại yêu cầu của lần triển khai web ban đầu; không dùng nó làm runtime authority hay chạy lại như một task hiện tại. Các số phiên bản, model, dependency, phạm vi file và lệnh bên dưới là ví dụ lịch sử. Hãy dùng manifest, mã nguồn, cấu hình deploy hiện tại và `web/README.md` để xác định hành vi hiện hành.

Đây là prompt để giao cho Gemini thực thi. Đọc `PLAN.md` trước khi dùng prompt này.

---

## Context

Bạn đang làm việc trong monorepo `vietnamese-humanizer` (Python package cung cấp Agent Skills + linter văn phong tiếng Việt). Package gốc (đã hoàn chỉnh, không sửa) nằm ở `src/`, `patterns/`, `skills/`, `examples/`, `benchmarks/`, `tests/`. 

Nhiệm vụ của bạn là xây dựng toàn bộ phần `web/` (backend + frontend) cho web app "Vietnamese Writing Skills" — một trang web để kiểm tra và gợi ý sửa văn phong tiếng Việt, dựa trên chính package này.

## Các nguyên tắc BẮT BUỘC (đọc kỹ, vi phạm = THẤT BẠI)

1. **Không sửa bất kỳ file nào ngoài `web/`**, trừ: thêm `.github/workflows/web-ci.yml` (workflow CI riêng) và đã có sẵn `.gitignore` cập nhật.
2. **Không sửa `src/`, `patterns/`, `skills/`, `examples/`, `benchmarks/`, `tests/`, `pyproject.toml`, `README.md`, `docs/`, `scripts/`.**
3. **Backend chỉ TIÊU THỤ package qua import.** Cài `vietnamese-writing-skills` như dependency trong `web/backend/pyproject.toml`. Import public API:
   - `from vietnamese_writing_skills.cli.lint import lint_text`
   - `from vietnamese_writing_skills.core.patterns import pattern_index, iter_patterns`
   - `from vietnamese_writing_skills import __version__`
4. **Không phân loại tác giả, không AI-probability score.** UI không hiển thị "X% do AI viết". Ghi rõ: đây là công cụ nêu tín hiệu văn phong để con người review, KHÔNG phải AI-detector.
5. **Chức năng "rewrite"** (generative, gọi Gemini API) BẮT BUỘC gắn nhãn `review_status: "unreviewed"` và disclaimer "gợi ý cần review". Hiển thị diff, không tự động thay thế. `/api/lint` = bắt lỗi (deterministic); `/api/rewrite` = Gemini viết lại (generative).
6. **Test của web nằm riêng:** `web/backend/tests` — pytest riêng, không trộn vào `tests/` gốc. CI gốc `.github/workflows/ci.yml` phải giữ nguyên hành vi (không đổi).
7. **Không ghi dữ liệu người dùng vào corpus.** Feature đóng góp case lưu vào DATABASE (staging), KHÔNG append vào `examples/examples.jsonl` hoặc `benchmarks/`. Maintainer duyệt trong DB rồi tự làm PR.
8. **Rate limit áp dụng NGAY từ đầu cho MỌI endpoint** (slowapi). Endpoint admin bắt buộc auth qua `ADMIN_API_KEY`.

## Kiến trúc cần xây

```
web/
├── PLAN.md                      (đã có — đọc làm reference)
├── GEMINI_PROMPT.md            (file này)
├── README.md                   (hướng dẫn chạy local + deploy)
├── backend/
│   ├── app/
│   │   ├── main.py             (FastAPI app, CORS, include routers)
│   │   ├── config.py           (Settings từ env: CORS_ORIGINS, GEMINI_API_KEY, LINT_MAX_CHARS, ...)
│   │   ├── schemas.py          (Pydantic: LintRequest, LintResponse, RewriteRequest, ...)
│   │   ├── limiter.py          (slowapi Limiter dùng chung, key theo IP)
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── health.py       (GET /api/health → {version, status})
│   │   │   ├── lint.py         (POST /api/lint — deterministic, bắt lỗi)
│   │   │   ├── patterns.py     (GET /api/patterns, /api/skills)
│   │   │   ├── rewrite.py      (POST /api/rewrite — Gemini viết lại)
│   │   │   ├── contributions.py (POST /api/contributions — user gửi case)
│   │   │   └── admin.py        (GET/PATCH /api/admin/contributions — duyệt, auth)
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── database.py     (SQLAlchemy engine/session từ DATABASE_URL; SQLite khi dev)
│   │   │   └── models.py       (model Contribution + enum status)
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── linter.py       (wrap lint_text, pattern_index)
│   │       ├── rewriter.py     (gọi Gemini với SKILL.md context)
│   │       └── contributions.py (CRUD staging, export approved)
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py         (fixture TestClient + SQLite tạm + mock Gemini)
│   │   ├── test_lint.py        (test /api/lint với fixture text)
│   │   ├── test_patterns.py    (test /api/patterns trả đúng cấu trúc)
│   │   ├── test_rewrite.py     (mock Gemini; assert review_status=unreviewed)
│   │   ├── test_contributions.py (submit + validate consent + rate limit)
│   │   └── test_admin.py       (401 khi thiếu key; duyệt khi đúng key)
│   ├── pyproject.toml          (deps: fastapi, uvicorn, pydantic-settings, slowapi, sqlalchemy, vietnamese-writing-skills==0.2.0, google-genai, pytest, httpx)
│   ├── requirements.txt        (generate từ pyproject hoặc tay; cho Render)
│   ├── render.yaml             (blueprint: service Python web + Postgres, root=web/backend)
│   ├── .env.example            (FRONTEND_ORIGIN, GEMINI_API_KEY, ADMIN_API_KEY, DATABASE_URL, LINT_MAX_CHARS)
│   └── README.md               (dev: pip install -e ., uvicorn app.main:app --reload)
└── frontend/
    ├── app/
    │   ├── page.tsx            (trang chính: editor + results + rewrite)
    │   ├── contribute/page.tsx (trang đóng góp case)
    │   ├── layout.tsx          (root layout, metadata, Tailwind, font)
    │   └── globals.css         (Tailwind directives)
    ├── components/
    │   ├── Editor.tsx          (textarea input, chọn skills, nút Kiểm tra)
    │   ├── IssueList.tsx       (list issue theo finding_type)
    │   ├── IssueCard.tsx       (hiển thị 1 issue + badge severity)
    │   ├── RewritePanel.tsx    (diff gốc vs gợi ý Gemini + nhãn cần review)
    │   ├── ContributeForm.tsx  (form gửi case + checkbox consent bắt buộc)
    │   └── Disclaimer.tsx      (banner: không phải AI-detector)
    ├── lib/
    │   ├── api.ts              (fetch /api/lint, /api/patterns, /api/rewrite, /api/contributions)
    │   └── types.ts            (mirror backend schemas)
    ├── public/
    ├── package.json            (deps: next, react, react-dom, tailwindcss, typescript)
    ├── tsconfig.json
    ├── next.config.js
    ├── tailwind.config.ts
    ├── postcss.config.js
    ├── .env.local.example      (NEXT_PUBLIC_API_BASE_URL)
    └── README.md               (dev: npm install, npm run dev)
```

## Hợp đồng API Backend (chi tiết)

### `GET /api/health`
Response: `{"status": "ok", "version": "0.2.0"}` (lấy `__version__` từ package)

### `POST /api/lint`
Request:
```json
{
  "text": "string (required, max 20000 chars)",
  "skills": ["humanizer-vi", "style-guide-vi"] | null
}
```
- Validate: `text` không rỗng, skills chỉ nhận giá trị trong: `humanizer-vi, translationese-cleaner-vi, grammar-checker-vi, style-guide-vi`.
- Gọi `lint_text(text, skills=set(skills) if skills else None)`.
- Trả:
```json
{
  "version": "0.2.0",
  "summary": {
    "total": 5,
    "error": 0, "warning": 2, "preference": 0, "heuristic": 3,
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
      "excerpt": "...",
      "message": "...",
      "suggestion": "..."
    }
  ]
}
```

### `GET /api/patterns`
- Gọi `pattern_index()`, filter chỉ trả: `id, name, skill, category, finding_type, severity, summary, why_it_matters, rewrite_strategy[0]`.
- Response: `{"patterns": [...]}`

### `GET /api/skills`
Response:
```json
{
  "skills": [
    {
      "id": "humanizer-vi",
      "name": "Humanizer tiếng Việt",
      "when_to_use": "Văn bản có vẻ theo khuôn, sáo, đều nhịp hoặc lệch giọng",
      "when_not_to_use": "Suy đoán tác giả, lách detector, hoặc chỉ soát lỗi máy móc"
    },
    ...
  ]
}
```
(hard-code 4 skill từ bảng trong README hoặc parse từ `skills/*/SKILL.md` frontmatter)

### `POST /api/rewrite` (optional)
Request:
```json
{
  "text": "string",
  "skill": "humanizer-vi",
  "issue_ids": ["VI-HUM-L02"] | null
}
```
Logic (trong `rewriter.py`):
1. Chạy `lint_text` → lấy issue match.
2. Đọc `SKILL.md` tương ứng qua helper của package (xử lý được cả source checkout lẫn wheel đã cài): `from vietnamese_writing_skills.core.paths import data_location` rồi `data_location('skills') / skill / 'SKILL.md'`. Dùng `.read_text(encoding='utf-8')` (Path) hoặc `.read_text()` (Traversable). KHÔNG hardcode đường dẫn `data/skills/...` vì trong source checkout resource nằm ở repo root, còn trong wheel mới nằm dưới `data/`.
3. Lấy `rewrite_strategy` của các pattern liên quan.
4. System prompt Gemini: "Bạn là biên tập viên tiếng Việt. Sửa văn bản theo hướng dẫn skill và danh sách issue, nhưng BẮT BUỘC bảo toàn: dữ kiện, số liệu, tên riêng, mức độ chắc chắn, thuật ngữ chuyên môn. Không thêm ví dụ/nguồn/metric mới. Trả lại chỉ văn bản đã sửa, không giải thích."
5. Gọi Gemini API. **Ưu tiên SDK mới `google-genai`** (`from google import genai`; model `gemini-2.0-flash` hoặc mới hơn) thay vì `google-generativeai` cũ đã deprecated. Chọn 1 SDK và ghi đúng vào `pyproject.toml`.
6. Response:
```json
{
  "rewrite": "...",
  "review_status": "unreviewed",
  "disclaimer": "Gợi ý do model sinh, cần người đọc kiểm chứng bảo toàn dữ kiện."
}
```
- Nếu `GEMINI_API_KEY` không có → 503 với message rõ (phần `/api/lint` vẫn chạy bình thường).
- Rate limit: 5 request/phút/IP (chặt vì tốn token Gemini).

### `POST /api/contributions` (public, rate-limit mạnh)
Cho phép người dùng gửi case đề xuất. **Lưu vào DATABASE (staging), KHÔNG ghi vào file corpus.**

Request:
```json
{
  "input_text": "string (required)",
  "context": "string (optional)",
  "suggestion": "string (required)",
  "skill": "humanizer-vi",
  "pattern_ids": ["VI-HUM-L02"] | null,
  "note": "string (optional)",
  "consent": true
}
```
Logic (trong `services/contributions.py`):
1. Validate: `consent` phải `true` (nếu false/thiếu → HTTP 400). `skill` trong tập hợp lệ. Giới hạn độ dài từng field (ví dụ input/suggestion ≤ 20000, context/note ≤ 5000).
2. Lưu row vào bảng `contributions` với `status="pending"`, `created_at=now()`.
3. Response: `{"id": "...", "status": "pending", "message": "Cảm ơn đóng góp, sẽ được maintainer xem xét."}`.
- Rate limit: 3 req/phút/IP.
- KHÔNG có endpoint public để đọc contribution của người khác (tránh biến thành nơi đăng nội dung tùy ý).

### Model `Contribution` (SQLAlchemy, trong `db/models.py`)
Cột: `id` (PK), `created_at`, `input_text`, `context`, `suggestion`, `skill`, `pattern_ids` (JSON/text), `note`, `consent` (bool), `status` (`pending`/`approved`/`rejected`, default `pending`), `review_note`, `reviewed_at`.

`db/database.py`: đọc `DATABASE_URL` (Postgres trên Render; SQLite `sqlite:///./dev.db` khi dev/test). Tạo bảng bằng `Base.metadata.create_all()` lúc startup.

### Admin endpoints (cần auth `X-Admin-Key` == env `ADMIN_API_KEY`)
Dùng FastAPI dependency kiểm tra header; sai/thiếu → HTTP 401.
- `GET /api/admin/contributions?status=pending` → list contributions để duyệt.
- `PATCH /api/admin/contributions/{id}` → body `{"status": "approved"|"rejected", "review_note": "..."}`, cập nhật `reviewed_at`.
- `GET /api/admin/contributions/export?status=approved` → xuất JSON các case đã duyệt (nguyên liệu để maintainer tự làm PR corpus). Endpoint này KHÔNG ghi vào file repo.

### Rate limit (slowapi — áp dụng NGAY từ đầu cho MỌI endpoint)
- Tạo `app/limiter.py`: `Limiter(key_func=get_remote_address)`. Gắn vào app, thêm exception handler cho `RateLimitExceeded` (trả 429).
- Ngưỡng: lint 30/phút, patterns+skills 60/phút, rewrite 5/phút, contributions 3/phút. Admin không cần limit (đã có auth).
- Trên Render (sau proxy), cấu hình đọc IP thật từ `X-Forwarded-For` (dùng `ProxyHeadersMiddleware` của uvicorn hoặc trusted hosts).

## Frontend — yêu cầu UX

- Next.js App Router + TypeScript + Tailwind.
- **Trang chính (`app/page.tsx`):**
  - Component `<Disclaimer />` trên cùng: "Công cụ nêu tín hiệu văn phong, KHÔNG phải AI-detector, không chấm điểm AI."
  - `<Editor />`: textarea lớn, checkbox 4 skill (mặc định chọn tất cả), nút "Kiểm tra".
  - `<IssueList />`: sau khi submit, hiển thị summary (`total, error/warning/preference/heuristic`) + danh sách `<IssueCard />`.
  - `<IssueCard />`: line:column, excerpt, message, suggestion, badge severity (màu: high=red, medium=yellow, low=blue).
  - Bấm vào issue → mở panel (modal hoặc expand) hiển thị chi tiết pattern từ `/api/patterns` (summary, why_it_matters).
  - `<RewritePanel />`: nút "Gợi ý viết lại" gọi `/api/rewrite`, hiển thị diff gốc vs gợi ý, gắn nhãn rõ ràng "gợi ý cần review" (không tự thay thế). Nếu backend trả 503 (thiếu key) → thông báo nhẹ nhàng, không crash.
- **Trang đóng góp (`app/contribute/page.tsx`):**
  - `<ContributeForm />`: các field input_text, context, suggestion, chọn skill, note; **checkbox consent bắt buộc tick** ("Tôi xác nhận không gửi thông tin cá nhân nhạy cảm và có quyền chia sẻ ví dụ này"). Nút submit disabled tới khi tick.
  - Gọi `POST /api/contributions`, hiển thị thông báo thành công (kèm id) hoặc lỗi (429 rate limit / 400 thiếu consent).
- i18n: mặc định tiếng Việt (label, message UI).
- Responsive: mobile-friendly.

## Các bước thực thi (tuần tự)

1. **Tạo cấu trúc thư mục** `web/backend/` và `web/frontend/` theo sơ đồ trên.
2. **Backend:**
   - Viết `pyproject.toml` với deps (fastapi, uvicorn, pydantic-settings, slowapi, sqlalchemy, vietnamese-writing-skills==0.2.0, google-genai, pytest, httpx).
   - `app/config.py`: `pydantic_settings.BaseSettings` đọc env (FRONTEND_ORIGIN, GEMINI_API_KEY, ADMIN_API_KEY, DATABASE_URL, LINT_MAX_CHARS).
   - `app/limiter.py`: slowapi Limiter dùng chung.
   - `app/db/database.py` + `app/db/models.py`: engine/session + model `Contribution`.
   - `app/schemas.py`: Pydantic models cho tất cả request/response.
   - `app/services/linter.py`: `lint_text_service(text, skills)` wrap `lint_text`, format response.
   - `app/services/rewriter.py`: gọi Gemini với SKILL.md context (bảo toàn dữ kiện).
   - `app/services/contributions.py`: CRUD staging + export approved.
   - `app/routers/`: `health.py`, `lint.py`, `patterns.py`, `rewrite.py`, `contributions.py`, `admin.py` — gắn rate limit cho từng endpoint.
   - `app/main.py`: khởi tạo FastAPI, CORS (đọc `FRONTEND_ORIGIN`), ProxyHeaders, gắn limiter + handler 429, include tất cả router, `create_all()` lúc startup.
   - `tests/`: `conftest.py` (TestClient + SQLite tạm + mock Gemini), `test_lint.py`, `test_patterns.py`, `test_rewrite.py`, `test_contributions.py`, `test_admin.py`.
   - `requirements.txt`: generate từ pyproject (`pip-compile` hoặc tay).
   - `render.yaml`: blueprint deploy web service + Postgres.
   - `.env.example`.
3. **Frontend:**
   - Init Next.js: `npx create-next-app@latest frontend --typescript --tailwind --app`.
   - Viết components: `Editor.tsx`, `IssueList.tsx`, `IssueCard.tsx`, `RewritePanel.tsx`, `ContributeForm.tsx`, `Disclaimer.tsx`.
   - `lib/api.ts`: fetch client (`POST /api/lint`, `GET /api/patterns`, `POST /api/rewrite`, `POST /api/contributions`).
   - `app/page.tsx` (check + rewrite) và `app/contribute/page.tsx` (đóng góp): orchestrate.
   - `.env.local.example`: `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`.
4. **CI cho web:**
   - Tạo `.github/workflows/web-ci.yml`:
     ```yaml
     name: Web CI
     on:
       push:
         paths: ['web/**']
       pull_request:
         paths: ['web/**']
     jobs:
       backend:
         runs-on: ubuntu-latest
         defaults:
           run:
             working-directory: web/backend
         steps:
           - uses: actions/checkout@v6
           - uses: actions/setup-python@v6
             with:
               python-version: "3.13"
           - run: pip install -e .
           - run: ruff check .
           - run: pytest
       frontend:
         runs-on: ubuntu-latest
         defaults:
           run:
             working-directory: web/frontend
         steps:
           - uses: actions/checkout@v6
           - uses: actions/setup-node@v4
             with:
               node-version: "20"
           - run: npm ci
           - run: npm run build
           - run: npm run lint
     ```
5. **Viết `web/README.md`:** hướng dẫn chạy local backend + frontend, env vars, deploy Render + Vercel.
6. **Kiểm tra không regression:**
   - `cd <root> && ruff check . && pytest` — phải xanh.
   - `git status` chỉ thấy thay đổi trong `web/`, `.gitignore`, `.github/workflows/web-ci.yml`.

## Văn bản mẫu để test

Dùng các fixture từ `tests/fixtures/` (ví dụ `natural_article.md`, `ai_generated.md`) hoặc tạo văn bản ngắn có pattern match:
```
Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới. Trong bối cảnh không ngừng phát triển, thị trường yêu cầu linh hoạt.
```
→ Phải match `VI-HUM-L02` (lời dẫn chung chung).

## Deliverable cuối cùng

- Toàn bộ code trong `web/`.
- Backend chạy local: `cd web/backend && uvicorn app.main:app --reload` → `http://localhost:8000/api/health` trả version.
- Frontend chạy local: `cd web/frontend && npm run dev` → `http://localhost:3000`, gọi được backend, hiển thị issue + disclaimer + rewrite + form đóng góp.
- `pytest` trong `web/backend/tests` xanh (test coverage: health, lint, patterns, rewrite mock, contributions + admin auth).
- Database tạo bảng tự động lúc startup (SQLite dev, Postgres prod).
- CI gốc không bị ảnh hưởng: `ruff check . && pytest` ở root vẫn xanh.
- `git diff` chỉ trong `web/`, `.gitignore`, `web-ci.yml`.

## Checklist cuối (verify trước khi commit)

- [ ] Không sửa `src/`, `patterns/`, `skills/`, `examples/`, `benchmarks/`, `tests/`, `pyproject.toml`, README gốc.
- [ ] Backend import package qua `pip install vietnamese-writing-skills`, không import trực tiếp từ `../../src`.
- [ ] `/api/lint` trả kết quả khớp với CLI `viet-writing-lint` trên cùng văn bản.
- [ ] `/api/rewrite` response bắt buộc gắn `review_status: "unreviewed"` + disclaimer; thiếu key → 503.
- [ ] `/api/contributions` lưu vào DB `status=pending`; từ chối khi `consent != true`; KHÔNG ghi vào `examples/` hay `benchmarks/`.
- [ ] `/api/admin/*` trả 401 khi thiếu/sai `ADMIN_API_KEY`.
- [ ] Rate limit hoạt động trên mọi endpoint public (vượt ngưỡng → 429).
- [ ] Frontend có disclaimer rõ ràng: không phải AI-detector; form đóng góp có checkbox consent bắt buộc.
- [ ] `pytest` gốc (`tests/`) và `pytest` web (`web/backend/tests`) đều xanh, tách biệt (test dùng SQLite tạm + mock Gemini).
- [ ] `web-ci.yml` chỉ trigger khi `web/**` thay đổi; `ci.yml` gốc không đổi.
- [ ] Không có AI-probability score hay tính năng "vượt detector" trong UI.

## Khi hoàn thành

Commit với message: `feat(web): add backend + frontend for Vietnamese Writing Skills web app`

Sau đó báo cáo:
1. Cấu trúc thư mục `web/` đã tạo.
2. Kết quả test backend (`pytest web/backend/tests`).
3. Kết quả CI gốc (`ruff check . && pytest` ở root).
4. Screenshot hoặc mô tả UI frontend (disclaimer, editor, issue list).
5. Hướng dẫn chạy local và deploy (trong `web/README.md`).

---

**Bắt đầu ngay bây giờ. Tuân thủ chặt chẽ các nguyên tắc BẮT BUỘC. Thành công = 100% code trong `web/`, 0% thay đổi bên ngoài (trừ `.gitignore` và `web-ci.yml`).**
