# Benchmark

Bộ benchmark gồm 30 case đa miền, tách theo bốn skill. Đây là đánh giá biên tập và preservation, không phải phép đo khả năng phát hiện văn bản do AI tạo.

Mỗi case có input, context, constraints, must-preserve, must-not-add và blockers. Case không nên sửa có thể để `expected_patterns` rỗng; không gán một pattern giả chỉ để buộc agent thay đổi câu.

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

Runner kiểm từng review, hỗ trợ nhiều reviewer cho một case, tính average theo tiêu chí, blocker rate, số case đã review và số case chưa review. Runner không tính agreement khi chưa có thiết kế đánh giá và overlap phù hợp.

Thư mục `results/` không có điểm baseline giả. Xem `results/README.md` để biết trạng thái review hiện tại.
