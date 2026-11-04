# Đánh giá writing profiles bằng người đọc thật

Trạng thái ngày 3 tháng 11 năm 2026: `cases/writing-profiles.jsonl` có 24 case tự viết, chia thành 12 cặp. Mỗi profile `plain`, `business`, `technical` có bốn cặp, gồm bốn bản phù hợp dự kiến giữ nguyên và bốn bản cần xử lý. Chưa có review độc lập, output từ model hoặc điểm baseline được công bố.

## Tạo đầu ra để so sánh

1. Cố định commit, phiên bản model, cấu hình sinh và nội dung prompt của từng hệ thống. Dùng mã hệ thống riêng cho baseline và phiên bản có profile; giữ mapping ngoài gói chấm mù.
2. Với mỗi case, gửi `input` thành `text`, kèm skill/context/style. Đưa constraints vào yêu cầu biên tập. Không đưa expected mode, must-preserve, must-not-add, evaluation notes hoặc blockers vào prompt sinh.
3. Khi đo tác động của profile, dùng cùng text/context/channel/register/edit_level và chỉ đổi `style.profile` thành `preserve` ở baseline. Lưu cả lỗi sinh, không bỏ những output xấu khỏi mẫu báo cáo.
4. Lưu output nguyên vẹn cùng metadata của lần sinh. Không lấy bản sửa minh họa trong reference làm đáp án mong đợi. Case mới dùng tình huống khác ví dụ trong reference; bộ nhỏ này vẫn chưa đại diện cho ngôn ngữ ngoài dự án.

## Chấm độc lập

Nhờ ít nhất hai người bản ngữ chấm cùng các output mà chưa trao đổi. Với profile kỹ thuật, cần ít nhất một người hiểu tài liệu kỹ thuật; ghi phạm vi kinh nghiệm và biến thể tiếng Việt họ dùng trong mô tả đợt đánh giá. Không suy đoán thông tin này từ tên reviewer.

Xáo thứ tự trình bày, giấu tên hệ thống và giữ nguyên input/context/yêu cầu người dùng để reviewer biết giọng cần đạt. Cho phép hòa và nhiều bản sửa cùng đúng. Mỗi reviewer kiểm blocker trước, rồi chấm tám tiêu chí của [review-result.schema.json](review-result.schema.json). Với output có blocker, vẫn ghi các điểm còn chấm được để giữ định dạng thống nhất; kết quả vẫn là fail, không dùng average để bù blocker.

| Tiêu chí | Câu hỏi cần trả lời theo profile |
| --- | --- |
| Naturalness, clarity | Văn viết có theo được mạch? Email có rõ việc? Hướng dẫn có rõ điều kiện và thao tác? |
| Meaning, factual preservation | Có giữ phủ định, giới hạn, mức chắc chắn và trạng thái chưa xong? |
| Register fit | Có hợp người đọc và quan hệ? Kỹ thuật + friendly có còn chính xác? Chat công việc có giữ xưng hô? |
| Terminology consistency | Có giữ thuật ngữ, tên riêng, nhãn UI và code? |
| Edit necessity, over-editing avoidance | Với bản vốn tốt, có tránh sửa thừa hoặc làm mất nhịp riêng? |

Ghi bất đồng về nhãn expected trong `notes`. Runner dùng nhãn hiện có để kiểm mode; đánh dấu `incorrect_output_mode` theo nhãn đó và nêu phản biện riêng, sau đó maintainer xem xét sửa nhãn ở một thay đổi dữ liệu có review. Không sửa nhãn giữa chừng rồi so sánh điểm với batch cũ.

## Tổng hợp và giới hạn

Dùng định dạng trong [expected/README.md](expected/README.md), lưu reviewer thật dưới mã ẩn danh và ghi rõ batch có reviewer con người hay agent. `reviewer_id` tự nó không chứng minh review độc lập. Điểm kiểm thử phần mềm là dữ liệu giả trong test, không được đưa vào `results/`.

```bash
python scripts/run_benchmarks.py --results my-reviews.jsonl --output benchmarks/results/summary.json
```

Report có `by_profile` là số case, và `profile_results` tách từng profile rồi từng system, gồm điểm, blocker rate, số reviewer và case chưa review. Profile chưa có review có `systems: {}`; không diễn giải thành điểm 0 hay chất lượng đạt yêu cầu. Average toàn cục là trung bình các dòng review, có thể gộp nhiều system; dùng phần tách theo system cho so sánh.

Báo số cặp, số case, số output lỗi và phân bố reviewer. Giữ cả cặp trong cùng development/test; không tính hai thành viên là hai tình huống độc lập. Mẫu này phù hợp tìm lỗi và sửa hướng dẫn; chưa đủ để tuyên bố profile nào tốt hơn ngoài phạm vi đã chấm. Giữ điểm thô, lý do và bất đồng; chưa tính inter-rater agreement.
