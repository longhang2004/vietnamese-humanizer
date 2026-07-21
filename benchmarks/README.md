# Benchmark

Bộ benchmark gồm 30 case đa miền, tách theo bốn skill. Bộ này đánh giá biên tập và preservation, không đo khả năng phát hiện văn bản do AI tạo.

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
