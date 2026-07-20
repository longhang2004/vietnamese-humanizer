# Benchmark

Bộ benchmark gồm 30 case đa miền, tách theo bốn skill. Đây là bộ đánh giá biên tập, không phải phép đo khả năng phát hiện văn bản do AI tạo.

Validate dữ liệu:

```bash
python scripts/run_benchmarks.py --validate-only
```

Reviewer có thể tạo JSONL kết quả theo mẫu trong `expected/README.md`, rồi chạy:

```bash
python scripts/run_benchmarks.py --results my-results.jsonl --output benchmarks/results/summary.json
```

Benchmark tách khỏi unit test vì output ngôn ngữ có nhiều phương án đúng. Unit test kiểm mã deterministic; benchmark cần đánh giá của người bản ngữ theo rubric.
