# Web app Vietnamese Writing Skills

Web app cung cấp linter deterministic, danh mục pattern và các tính năng viết lại, nhận đóng góp có thể bật riêng. Linter nêu tín hiệu để người viết review; ứng dụng không chấm xác suất AI hay suy đoán tác giả.

## Chạy local

Máy cần có Python 3.11 trở lên, Node.js 20 trở lên và npm. Từ root repository, chạy:

```bash
python3 scripts/dev.py demo
```

Đây là quickstart chính. Lệnh tự kiểm tra điều kiện, tạo hoặc sửa `.venv`, cài dependency bằng pip và `npm ci`, sau đó chạy backend tại `http://localhost:8000` và frontend tại `http://localhost:3000`. Có thể chạy lại setup; nhấn Ctrl-C để dừng cả hai server.

Demo chủ động đặt `REWRITE_ENABLED=false`, `CONTRIBUTIONS_ENABLED=false` và `ADMIN_API_ENABLED=false`. Vì vậy, luồng local mặc định chỉ cần linter, không cần API key hay database. Dùng `python3 scripts/dev.py smoke` để setup, khởi động hai server, kiểm tra health/frontend/lint rồi tự dừng.

## Bật từng tính năng khi chạy thủ công

Sao chép `web/backend/.env.example` thành `web/backend/.env` và `web/frontend/.env.local.example` thành `web/frontend/.env.local`, sau đó chỉ bật tính năng cần dùng.

| Tính năng | Biến cấu hình | Hành vi |
| --- | --- | --- |
| Lint và metadata | `FRONTEND_ORIGIN`, `LINT_MAX_CHARS` | Luôn bật. Backend xử lý text để trả finding; mã nguồn dự án không biến input lint thành contribution. |
| Viết lại | `REWRITE_ENABLED=true`, `GEMINI_API_KEY` không rỗng | Mặc định tắt. Text viết lại được gửi tới tích hợp Gemini; output luôn cần người dùng review. |
| Nhận đóng góp | `CONTRIBUTIONS_ENABLED=true`, `DATABASE_URL` | Mặc định tắt. Submission được lưu để maintainer review, không tự động thành corpus hay dữ liệu huấn luyện. |
| Admin | `ADMIN_API_ENABLED=true`, `DATABASE_URL`, `ADMIN_API_KEY` | Mặc định tắt. Key phải không phải placeholder, dài tối thiểu 32 ký tự và được gửi qua header `X-Admin-Key`. |
| Frontend | `NEXT_PUBLIC_API_BASE_URL`; tùy chọn `NEXT_PUBLIC_SITE_URL` | Chọn backend URL và metadata base URL. |

Nếu một flag bị tắt, route tương ứng trả `503`. Bật rewrite mà thiếu key, hoặc bật admin với key ngắn/placeholder, là cấu hình không hợp lệ và backend không khởi động.

Khi cần chạy từng service sau khi đã setup:

```bash
cd web/backend
../../.venv/bin/python -m uvicorn app.main:app --reload --port 8000
```

```bash
cd web/frontend
npm run dev
```

## Dữ liệu đóng góp và analytics

Database contribution chỉ là vùng staging. Việc duyệt hoặc export không ghi vào `examples/` hay `benchmarks/`; muốn đưa nội dung vào corpus vẫn phải chuẩn hóa, bỏ dữ liệu nhạy cảm, review và mở pull request theo `CONTRIBUTING.vi.md`.

Wave 1 giữ dependency Vercel Analytics và render `<Analytics />`. Mã nguồn dự án không gửi custom event, user ID, văn bản document/lint/rewrite/contribution hay thuộc tính suy ra từ văn bản qua custom analytics event. Không suy rộng phát biểu này thành cam kết về retention của nhà cung cấp, log hosting, mã hóa, APM hay cấu hình của một deployment.

## Deploy và kiểm tra

`web/backend/render.yaml` là cấu hình Render hiện có: nó bật contribution/admin và nhận `DATABASE_URL` từ database đã khai báo, nhưng không bật rewrite. Frontend dùng `NEXT_PUBLIC_API_BASE_URL` để chọn backend. Các file này không chứng minh trạng thái hay thuộc tính bảo mật của deployment đang chạy.

Từ root repository:

```bash
python3 scripts/dev.py check
python3 scripts/dev.py smoke --skip-setup
git diff --check
```

Xem [hướng dẫn maintainer](../docs/maintainer-guide.md) để biết nội dung từng quality gate và quy trình review contribution.
