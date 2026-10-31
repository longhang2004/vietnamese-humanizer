# Benchmark

Bộ benchmark gồm 70 case đa miền cho bốn skill. Bộ này đánh giá biên tập và preservation, không đo khả năng phát hiện văn bản do AI tạo.

`cases/naturalness.jsonl` bổ sung 30 case dài 150–500 đơn vị tách bằng khoảng trắng (không phải đếm từ bằng word segmentation), theo 15 cặp: bản phù hợp cần giữ nguyên và bản có vấn đề cần sửa/góp ý/hỏi tác giả. Trường `style` tùy chọn dùng cùng các lựa chọn với API rewrite. Tất cả tài liệu mới do coding agent tự viết; chưa có human review hoặc điểm baseline. Đây là bộ nhỏ có cặp phụ thuộc, không phải 30 mẫu độc lập đại diện tiếng Việt.

Khi chạy một case qua API, chuyển `input` thành `text`, giữ nguyên `context` và `style`, đồng thời đưa yêu cầu biên tập trong `constraints` vào context. Không đưa expected mode, blocker hoặc evaluation notes vào prompt sinh. Khi chia development/test, giữ cả cặp trong cùng một phần.

Mỗi case có input, context, constraints, expected output mode, must-preserve, must-not-add và blockers. Case không nên sửa dùng `no_change` và có thể để `expected_patterns` rỗng. Không gán pattern giả chỉ để buộc agent thay đổi câu.

Validate dữ liệu:

```bash
python scripts/run_benchmarks.py --validate-only
```

Reviewer tạo JSONL theo `review-result.schema.json` và hướng dẫn trong `expected/README.md`, rồi chạy:

```bash
python scripts/run_benchmarks.py \
  --results my-reviews.jsonl \
  --output benchmarks/results/summary.json
```

Runner kiểm từng review. Actual output mode phải khớp expected mode hoặc có blocker `incorrect_output_mode`. Runner hỗ trợ nhiều reviewer cho một case và tính average theo tiêu chí, blocker rate, số case đã review, số case chưa review. Khi chưa có thiết kế đánh giá và overlap phù hợp, runner không tính agreement.

Thư mục `results/` không có điểm baseline giả. Xem `results/README.md` để biết trạng thái review hiện tại.
