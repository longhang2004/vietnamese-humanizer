# Định dạng kết quả review

Mỗi dòng JSONL cần có `case_id`, `system`, `reviewer_id`, output mode thực tế, `output_mode_correct`, tám điểm, danh sách blocker và notes.

```json
{
  "case_id": "BENCH-HUM-001",
  "system": "model-name-or-agent",
  "reviewer_id": "reviewer-01",
  "output_mode": "clean_rewrite",
  "output_mode_correct": true,
  "scores": {
    "naturalness": 4,
    "clarity": 5,
    "meaning_preservation": 5,
    "factual_preservation": 5,
    "register_fit": 4,
    "terminology_consistency": 5,
    "edit_necessity": 4,
    "over_editing_avoidance": 5
  },
  "blockers": [],
  "notes": ""
}
```

Blocker dùng enum trong `../review-result.schema.json`. Nếu output mode không khớp case, reviewer đặt `output_mode_correct: false` và thêm `incorrect_output_mode`. Nếu output thêm dữ kiện, đổi số, tên, ngày, mức chắc chắn, lập trường, nguồn, điều kiện, ngoại lệ, thuật ngữ, trải nghiệm, nguyên nhân hoặc metric thì reviewer phải đánh dấu blocker dù các điểm khác cao.

Nhiều bản sửa có thể đạt yêu cầu nên repository không lưu một đáp án vàng duy nhất. Không điền điểm mẫu vào `results/` nếu chưa có reviewer thật.
