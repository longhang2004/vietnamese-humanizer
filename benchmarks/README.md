# Benchmark

Bộ benchmark gồm 151 case đa miền cho bốn skill. Bộ này đánh giá biên tập và preservation, không đo khả năng phát hiện văn bản do AI tạo.

`cases/report-and-research.jsonl` có sáu tình huống giả định về báo cáo tiến độ, số liệu sơ bộ, mô phỏng, phỏng vấn và phạm vi kết luận. Bộ này có bản cần sửa, bản nên giữ nguyên và bản cần góp ý về bằng chứng. [Ghi chú nguồn và kiểm chứng](../docs/research/2026-11-22-report-and-research.md)

`cases/marketing-editorial-styles.jsonl` có năm tình huống giả định về câu hỏi theo tình huống, câu cảm thán báo tin, phủ định có nghĩa và vị trí điều kiện/chú thích. Ba bản dự kiến giữ nguyên, hai bản cần sửa. Xem [ghi chú nguồn và kiểm chứng](../docs/research/2026-11-22-marketing-voice.md).

`cases/editorial-restraint.jsonl` có bốn tình huống giả định về chuyển chủ thể trong bài kể và mốc chờ trong hướng dẫn. Mỗi profile có một case cần sửa và một case cần giữ nguyên. Nhãn dự kiến do agent đặt. Xem [ghi chú đọc nguồn và kiểm chứng](../docs/research/2026-11-21-vietnamese-voice.md).

`cases/naturalness.jsonl` bổ sung 30 case dài 150–500 đơn vị tách bằng khoảng trắng (không phải đếm từ bằng word segmentation), theo 15 cặp: bản phù hợp cần giữ nguyên và bản có vấn đề cần sửa/góp ý/hỏi tác giả. Trường `style` tùy chọn dùng cùng các lựa chọn với API rewrite. Tất cả tài liệu mới do coding agent tự viết; chưa có human review hoặc điểm baseline. Đây là bộ nhỏ có cặp phụ thuộc, không phải 30 mẫu độc lập đại diện tiếng Việt.

`cases/writing-profiles.jsonl` thêm 24 case ngắn và nhiều đoạn theo 12 cặp cho `plain`, `business`, `technical`; mỗi profile có bốn bản dự kiến giữ nguyên. Case kiểm bảo toàn giọng cá nhân, thời hạn, cam kết, điều kiện và code. Có tình huống kỹ thuật + friendly và công việc + chat để kiểm các lựa chọn độc lập. Các case do agent viết, chưa có human review. Xem [quy trình chấm độc lập](profile-review.md).

`cases/formulaic-prose.jsonl` thêm 12 case tự viết thành sáu cặp đối chiếu ngữ cảnh: đối lập, tóm tắt, chia mục, lời nhấn ý, lời trợ lý và ba thao tác kèm khoảng ước lượng. Mỗi cặp có trường hợp cần sửa và cần giữ; ngữ cảnh có thể khác để kiểm chức năng, không phải A/B cùng brief. Chưa có output được reviewer độc lập chấm. Xem [nguồn khảo sát và quyết định vận dụng](../docs/research/2026-11-04-formulaic-prose.md).

`cases/extended-profiles.jsonl` thêm 18 case theo chín cặp đối chiếu ngữ cảnh cho `administrative`, `social`, `marketing`. Mỗi profile có sáu case: ba bản giữ nguyên cùng ba tình huống sửa, góp ý và cần tác giả quyết định. Kiểm loại văn bản, nghĩa vụ, giọng cá nhân, chứng cứ, giá và điều kiện; đây là case tự viết, chưa có human review. Xem [nguồn đọc](../docs/research/2026-11-04-administrative-social-marketing.md).

`cases/voice-and-linguistics.jsonl` thêm 12 case theo sáu cặp đối chiếu ngữ cảnh cho `voice_sample`, cấu trúc Đề – Thuyết, chuỗi vị từ, phương ngữ kèm phân tầng Hán-Việt, calque dịch máy (`cho thấy rằng`, `cho phép`, `một cách + tính từ`), trượt ngôi tự xưng `tôi`/`mình` và liên từ kết quả thừa `vì vậy, nên`. Đây là case do agent tự viết để kiểm bảo toàn và ranh giới không sửa quá tay, chưa có human review.

Khi chạy một case qua API, chuyển `input` thành `text`, giữ nguyên `context` và `style`, đồng thời đưa yêu cầu biên tập trong `constraints` vào context. Không đưa expected mode, blocker hoặc evaluation notes vào prompt sinh. Khi chia development/test, giữ cả cặp trong cùng một phần. Có thể xuất sẵn gói đầu vào chấm mù không chứa đáp án bằng:

```bash
python scripts/run_benchmarks.py --prepare-packet /tmp/review-packet.jsonl
```

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

`by_profile` đếm case theo `style.profile`; case không chọn profile được tính là `preserve`. Khi có kết quả, `profile_results` tách review theo profile và system, gồm điểm, blocker rate và độ phủ. Profile chưa chấm có `systems: {}`; không sinh điểm mặc định. Average toàn cục vẫn gộp mọi dòng review; dùng phần theo system khi so sánh phiên bản.

Thư mục `results/` không có điểm baseline giả. Xem `results/README.md` để biết trạng thái review hiện tại.
