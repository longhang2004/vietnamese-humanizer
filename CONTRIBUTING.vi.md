[English](CONTRIBUTING.md) | **Tiếng Việt**

# Đóng góp

Cảm ơn bạn đã giúp Vietnamese Writing Skills phản ánh tiếng Việt đa dạng hơn.

## Trước khi mở pull request

1. Tìm ID, tên và tín hiệu tương tự trong `docs/generated-patterns.md`.
2. Đọc `docs/pattern-authoring-guide.md`.
3. Ẩn thông tin cá nhân và kiểm quyền sử dụng ví dụ.
4. Sửa dữ liệu, package, test và tài liệu liên quan.
5. Chạy generator, validators, test và build trong README.
6. Ghi thay đổi người dùng thấy được vào `CHANGELOG.md`.

## Example mới

Mỗi example phải có:

- input và context đầy đủ để output có thể được kiểm chứng;
- output không thêm dữ kiện, metric, nguồn, nguyên nhân hoặc trải nghiệm;
- `output_mode`, `gold_output_mode` và `gold_rewrite` nhất quán;
- `must_preserve` và `must_not_add`;
- pattern ID tồn tại;
- `preservation_review` với trạng thái và provenance đúng: `unreviewed`, `agent-reviewed`, `maintainer-reviewed` hoặc `independently-reviewed`;
- review notes khi đã reviewed.

Example `unreviewed` không được đánh dấu gold rewrite. `review_comment` và `needs_author_decision` có thể là gold output mode nhưng không phải gold rewrite. Đừng ghi “chi tiết đã có trong bài” nếu phần bài đó không nằm trong context.

## Pattern mới

Pattern cần finding type, scope, aggregation, severity, confidence, false-positive risk, hai bad example, hai good example có mode, exceptions, test và example không tự thêm dữ kiện. Nêu nguồn quan sát và phản biện trường hợp cấu trúc hợp lệ.

Pattern dựa trên trực giác của một người có thể mở ở dạng proposal để thu thập thêm ví dụ, nhưng chưa nên đưa vào catalog stable.

## Quy ước

- ID theo namespace `VI-HUM`, `VI-TRA`, `VI-GRA` hoặc `VI-STY`.
- `name` dùng chữ thường ASCII và dấu gạch nối.
- Tài liệu cho người dùng viết bằng tiếng Việt; identifier và thuật ngữ kỹ thuật có thể giữ tiếng Anh.
- Không thêm score phát hiện AI, claim bypass detector hoặc heuristic nhằm né kiểm tra.
- Không coi khác biệt vùng miền là lỗi nếu không có ràng buộc register cụ thể.
- Logic importable nằm trong `vietnamese_writing_skills`; `scripts/` chỉ chứa wrapper.

## Báo lỗi và đánh giá

Với false positive, cung cấp đoạn tối thiểu còn đủ context, domain, register, finding type, output mong muốn và lý do cấu trúc hợp lệ. Không gửi dữ liệu nhạy cảm.

## Checklist phát hành

Trước khi đẩy release tag:

1. Xác nhận CI trên `main` đang xanh.
2. Xác nhận version trong `pyproject.toml`, `vietnamese_writing_skills.__version__` và `CHANGELOG.md` khớp nhau.
3. Chạy toàn bộ kiểm tra repository, build wheel và sdist, rồi chạy `twine check dist/*`.
4. Xác nhận GitHub environment `pypi` và PyPI Trusted Publisher trỏ đến `.github/workflows/release.yml`.
5. Kiểm tra nội dung wheel và cài thử trong virtual environment sạch.
6. Chỉ đẩy tag `vX.Y.Z` tương ứng sau khi mọi kiểm tra đạt.
