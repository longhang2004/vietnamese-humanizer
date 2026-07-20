# Định dạng kết quả review

Mỗi dòng JSONL cần có `id`, `output`, tám điểm trong `scores`, tám cờ trong `blockers` và `notes`.

```json
{"id":"BENCH-HUM-001","output":"...","scores":{"naturalness":5,"clarity":5,"meaning_preservation":5,"factual_preservation":5,"register_fit":5,"terminology_consistency":5,"edit_necessity":5,"over_editing_avoidance":5},"blockers":{"fabricated_fact":false,"changed_number":false,"changed_proper_name":false,"changed_certainty":false,"changed_stance":false,"invented_source":false,"removed_condition":false,"incorrect_terminology":false},"notes":"..."}
```

Thư mục này không chứa một "đáp án vàng" duy nhất vì nhiều bản sửa có thể đạt yêu cầu. Maintainer có thể thêm các output đã được ít nhất hai reviewer bản ngữ duyệt ở phiên bản sau.
