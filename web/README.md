# Web App "Vietnamese Writing Skills"

Trang web ứng dụng hỗ trợ **kiểm tra tín hiệu văn phong** và **gợi ý gọt giũa tiếng Việt**, sử dụng trực tiếp bộ package `vietnamese-writing-skills` và tích hợp Gemini API cho tính năng viết lại thử nghiệm.

---

## ⚠️ Nguyên tắc cốt lõi

1. **Không phân loại tác giả, không AI-probability score**: Trang web nêu các tín hiệu bề mặt giúp người viết tự review, **KHÔNG** chấm điểm hay kết luận "X% do AI viết".
2. **Deterministic Check vs Generative Rewrite**:
   - `/api/lint`: Chạy quy tắc linter deterministic của package gốc.
   - `/api/rewrite`: Gọi Gemini API sinh bản gợi ý, **BẮT BUỘC** đi kèm nhãn `review_status: unreviewed` và disclaimer.
3. **Bảo tồn Corpus**: Đóng góp case của người dùng (`POST /api/contributions`) được lưu vào CSDL Staging (`contributions`), **KHÔNG** tự động ghi vào các file JSONL corpus (`examples/` hay `benchmarks/`).
4. **Thiết kế Anti-Slop & Chuẩn văn phong tiếng Việt (v0.4.0)**:
   - Giao diện biên tập hiện đại sử dụng bộ font `Plus Jakarta Sans` (nội dung/tiêu đề) và `JetBrains Mono` (mã pattern, dòng/cột).
   - Microcopy và nhãn UI tuân thủ 100% quy chuẩn diễn đạt tự nhiên, trực tiếp và câu chủ động của `vietnamese-writing-skills`.

---

## Cấu trúc thư mục

```
web/
├── PLAN.md                   # Tài liệu kế hoạch chi tiết
├── GEMINI_PROMPT.md          # Prompt chỉ dẫn thực thi
├── README.md                 # Hướng dẫn này
├── backend/                  # FastAPI backend service
│   ├── api/index.py          # Entry point cho Vercel Serverless Function
│   ├── vercel.json           # Cấu hình Vercel Python Function
│   ├── app/                  # Mã nguồn FastAPI app, config, schemas, DB, routers
│   ├── tests/                # Pytest riêng cho backend
│   ├── pyproject.toml        # Dependencies backend
│   ├── requirements.txt      # Cho Serverless / Render deployment
│   └── render.yaml           # Render Blueprint (nếu dùng Render)
└── frontend/                 # Next.js App Router frontend
    ├── app/                  # Pages (/ và /contribute)
    ├── components/           # UI Components (Editor, IssueList, RewritePanel, ...)
    ├── lib/                  # Fetch API client & TypeScript types
    └── package.json          # Dependencies Next.js & Tailwind
```

---

## 🚀 Hướng dẫn chạy Local Development

### 1. Khởi chạy Backend (FastAPI)

```bash
# 1. Cài đặt package gốc ở chế độ editable
pip install -e .

# 2. Chuyển vào thư mục backend và cài đặt dependencies
cd web/backend
pip install -e .

# 3. Tạo file cấu hình môi trường
cp .env.example .env

# 4. Khởi chạy Uvicorn server
uvicorn app.main:app --reload --port 8000
```

- API Health Check: `http://localhost:8000/api/health`
- OpenAPI Documentation: `http://localhost:8000/docs`

#### Chạy Tests Backend:

```bash
cd web/backend
pytest
```

---

### 2. Khởi chạy Frontend (Next.js)

```bash
# 1. Chuyển vào thư mục frontend
cd web/frontend

# 2. Cài đặt npm dependencies
npm install

# 3. Tạo file cấu hình môi trường local
cp .env.local.example .env.local

# 4. Khởi chạy dev server
npm run dev
```

Trang web sẽ sẵn sàng tại `http://localhost:3000`.

---

## 🚢 Hướng dẫn Deploy CẢ Frontend + Backend lên Vercel + Neon PostgreSQL

### Bước 1: Tạo Database trên Neon.tech
1. Đăng nhập [Neon.tech](https://neon.tech) -> Tạo Project mới.
2. Sao chép chuỗi kết nối **Connection String** (dạng `postgresql://user:password@ep-xyz.neon.tech/neondb?sslmode=require`).

### Bước 2: Deploy Backend (FastAPI) lên Vercel
1. Đăng nhập Vercel -> Chọn **Add New...** -> **Project**.
2. Chọn repository `vietnamese-humanizer`.
3. Đặt tên project (ví dụ: `vietnamese-writing-skills-api`).
4. **Root Directory**: Chọn `web/backend`.
5. **Environment Variables**:
   - `DATABASE_URL`: *(Dán Connection String từ Neon ở Bước 1)*
   - `GEMINI_API_KEY`: Key Gemini API của bạn.
   - `ADMIN_API_KEY`: Chuỗi secret key bảo vệ các route `/api/admin/*`.
   - `FRONTEND_ORIGIN`: URL domain frontend Vercel (hoặc `*`).
6. Bấm **Deploy**. Vercel sẽ tự động build Python backend và cấp URL (ví dụ `https://vietnamese-writing-skills-api.vercel.app`).

### Bước 3: Deploy Frontend (Next.js) lên Vercel
1. Trên Vercel -> Chọn **Add New...** -> **Project**.
2. Chọn lại repository `vietnamese-humanizer`.
3. Đặt tên project (ví dụ: `vietnamese-writing-skills-web`).
4. **Root Directory**: Chọn `web/frontend`.
5. **Environment Variables**:
   - `NEXT_PUBLIC_API_BASE_URL`: `https://vietnamese-writing-skills-api.vercel.app` *(URL Backend vừa deploy ở Bước 2)*.
6. Bấm **Deploy**. Trang web hoàn chỉnh sẽ hoạt động tại URL frontend.
