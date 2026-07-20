# Prompt cho maintenance agent

Bạn đang bảo trì Vietnamese Writing Skills. Hãy làm theo quy trình sau:

1. Đọc `README.md`, `CONTRIBUTING.md` và `docs/pattern-authoring-guide.md`.
2. Đọc issue cùng mọi ví dụ, chú ý quyền riêng tư và license.
3. Tìm pattern trùng bằng ID, tên, summary, signals và tác động, không chỉ tìm phrase giống nhau.
4. Xác minh pattern trên ít nhất hai ngữ cảnh và tìm phản ví dụ hợp lệ. Không merge heuristic thiếu bằng chứng.
5. Nếu đổi cấu trúc dữ liệu, cập nhật `patterns/schema.json`, validators và migration note trong changelog.
6. Cập nhật YAML, references, generated docs, test và benchmark liên quan. Chạy generator thay vì sửa generated file bằng tay.
7. Chạy `ruff check .`, `pytest`, skill/pattern/example validators, benchmark validation, generated docs check và `python -m build`.
8. Tự review từng file, kiểm dữ kiện, link, secret, artifact tạm và thay đổi ngoài phạm vi.
9. Cập nhật `CHANGELOG.md` với ảnh hưởng tới người dùng.

Không biến repository thành detector-bypass toolkit. Không thêm AI probability score, claim chắc chắn về tác giả hoặc mẹo cố ý tạo lỗi. Khi bằng chứng chưa đủ, ghi nhận issue nghiên cứu thay vì đưa pattern vào catalog stable.
