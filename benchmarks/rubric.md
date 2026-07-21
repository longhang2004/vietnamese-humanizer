# Rubric đánh giá

Chấm từng tiêu chí từ 1 đến 5.

| Tiêu chí | Điểm 1 | Điểm 3 | Điểm 5 |
| --- | --- | --- | --- |
| Naturalness | Gượng hoặc khó hiểu | Đọc được nhưng còn vài cấu trúc cứng | Tự nhiên với domain và độc giả |
| Clarity | Quan hệ ý bị che hoặc sai | Ý chính rõ, còn chỗ phải đọc lại | Chủ thể, hành động và logic đều rõ |
| Meaning preservation | Mất hoặc đổi ý chính | Giữ ý chính nhưng lệch một sắc thái nhỏ | Giữ đầy đủ ý, điều kiện và sắc thái |
| Factual preservation | Đổi hoặc bịa dữ kiện | Dữ kiện chính đúng, có chi tiết trình bày chưa chắc | Mọi dữ kiện, số và tên được giữ chính xác |
| Register fit | Sai hẳn quan hệ hoặc thể loại | Phần lớn phù hợp, đôi chỗ lệch | Phù hợp ổn định với thể loại và độc giả |
| Terminology consistency | Thuật ngữ sai hoặc loạn | Có một biến thể chưa cần thiết | Dùng đúng glossary và nhất quán |
| Edit necessity | Sửa nhiều chỗ vốn đã ổn | Phần lớn sửa có lý do | Mỗi thay đổi giải quyết vấn đề thật |
| Over-editing avoidance | Viết lại giọng hoặc mất chi tiết | Can thiệp hơi sâu nhưng chưa đổi nội dung | Giữ nguyên tối đa những phần đã tốt |

## Blocker

Output fail dù tổng điểm cao nếu sai output mode hoặc có một trong các lỗi sau: bịa dữ kiện; đổi số, tên riêng hoặc ngày tháng; đổi mức chắc chắn hoặc lập trường; thêm nguồn; xóa điều kiện hoặc ngoại lệ; làm sai thuật ngữ; thêm trải nghiệm cá nhân, nguyên nhân hoặc metric không có trong input/context.

Reviewer đánh dấu blocker trước khi cộng điểm. Một output có blocker không được dùng làm expected answer.

## Cách dùng điểm

Điểm 3 là bản dùng được sau một lượt sửa. Điểm 5 không đòi hỏi văn phong hoa mỹ; nó yêu cầu lựa chọn phù hợp và bảo toàn chặt. Với case "không sửa", thay đổi không cần thiết làm giảm Edit necessity và Over-editing avoidance.
