---
name: humanizer-vi
description: Biên tập tiếng Việt sáo, máy móc, đều nhịp hoặc lệch giọng để tự nhiên, rõ và hợp độc giả. Dùng khi chỉnh văn phong, bảo toàn giọng tác giả, hoặc biên tập chat và kịch bản nói theo yêu cầu. Không dùng để suy đoán tác giả, lách detector hay chỉ soát lỗi ngữ pháp.
license: MIT
metadata:
  language: vi
  version: "0.4.0"
---

# Humanizer tiếng Việt

Biên tập chất lượng viết, không phân loại nguồn gốc văn bản. Một tín hiệu đơn lẻ không đủ để kết luận có vấn đề. Ưu tiên cụm tín hiệu, tác động thật lên người đọc và mục đích của văn bản.

## Quy trình

1. Xác định loại văn bản, độc giả, mục đích và register. Nếu thiếu dữ kiện, suy ra từ văn bản và chọn mức can thiệp thấp.
2. Ghi nhận giọng hiện có: cách xưng hô, độ dài câu, mức trực tiếp, thuật ngữ và thói quen trình bày.
3. Đọc toàn đoạn trước khi sửa. Đánh dấu cấu trúc lặp, ý trừu tượng thiếu thông tin, lời dẫn chung chung, nhịp quá đều và giọng quảng cáo lệch ngữ cảnh.
4. Sửa cấu trúc câu và đoạn trước khi thay từ. Nêu hành động hoặc quan hệ logic trực tiếp; gộp hay tách câu khi giúp người đọc theo ý.
5. Giữ những câu đã ổn. Không sửa một cụm chỉ vì nó có trong catalog.
6. Rà lại đại từ, thuật ngữ và register. Đọc thành tiếng nếu nhịp câu là vấn đề.
7. Audit bản cuối theo danh sách bảo toàn. Chỉ giải thích thay đổi khi người dùng yêu cầu.

Đọc [workflow chi tiết](references/workflow.md) cho văn bản dài hoặc khi nhiều pattern chồng nhau. Tra [register](references/registers.md) trước khi sửa văn bản học thuật, pháp lý, hành chính hay chăm sóc khách hàng.

Đọc [diễn đạt tự nhiên](references/naturalness.md) khi chỉnh văn phong: tài liệu này hướng dẫn kết hợp từ, mạch thông tin, phép lặp và sắc thái. Chỉ đọc [hội thoại và kịch bản nói](references/conversational.md) khi người dùng chọn các kênh đó; văn viết gần gũi vẫn có tiêu chí riêng.

Khi người dùng chọn loại bài viết, đọc [writing profiles](references/writing-profiles.md) rồi chỉ đọc reference phù hợp: [văn viết rõ ràng](references/plain-writing.md), [trao đổi công việc](references/business-writing.md) hoặc [tài liệu kỹ thuật](references/technical-writing.md). Profile không tự đổi giọng, kênh, xưng hô hay mức can thiệp; mặc định giữ loại bài gốc.

## Ngữ cảnh và quyền biên tập

Phân biệt kênh (tài liệu, email, chat, kịch bản nói), độc giả, quan hệ giao tiếp, xưng hô và độ trang trọng. Chọn kênh chat không có nghĩa được đổi "tôi" thành "em" hoặc thêm "ạ". Khi thiếu thông tin, giữ giọng và xưng hô hiện có.

Mặc định sửa nhẹ. Chỉ sắp xếp lại đoạn khi người dùng cho phép can thiệp sâu; mọi mức đều phải giữ nội dung. Khi được yêu cầu giảm cường điệu (`reduce_hype=true` trong ứng dụng), có thể giảm tính từ quảng cáo hoặc đồng cảm công thức. Quyền này không cho phép đổi số, phạm vi, mức chắc chắn, nghĩa vụ hay lập trường tích cực thành tiêu cực. Nếu bỏ một nhận định sẽ đổi thông điệp, góp ý để tác giả quyết định.

## Bảo toàn

Giữ nguyên dữ kiện, con số, tên riêng, trích dẫn, điều kiện, ngoại lệ, lập trường, thuật ngữ và mức độ chắc chắn. Không đổi "có thể" thành "sẽ", không xóa giới hạn nghiên cứu và không thêm ví dụ để làm câu sinh động.

Chỉ dùng thông tin ngoài đoạn input khi nó được cung cấp rõ trong context. Không viện dẫn “chi tiết đã có trong bài” nếu phần bài đó không có trong dữ liệu đang review.

Khi một câu mơ hồ theo nhiều cách hợp lý, giữ nguyên phần mơ hồ hoặc hỏi lại nếu cách hiểu làm thay đổi kết quả đáng kể. Dùng checklist đầy đủ trong [preservation rules](references/preservation-rules.md).

## Cách chọn pattern

- Ưu tiên pattern làm mất thông tin hoặc làm sai register.
- Với từ nối, lời mở đầu, danh sách ba ý và nhịp câu, xét mật độ trên cả đoạn.
- Với lời dẫn nguồn mơ hồ, không tự bịa nguồn thay thế hoặc âm thầm hạ mức chắc chắn. Góp ý về bằng chứng còn thiếu; chỉ thu hẹp tuyên bố khi tác giả cho phép và context đủ căn cứ.
- Với giọng cá nhân, chỉ giữ hay tăng cá tính khi văn bản gốc đã có cơ sở. Văn bản trung lập không cần thêm "tôi".
- Nếu đầu vào tự nhiên và phù hợp, trả lại gần như nguyên văn.

Danh mục giải thích nằm ở [patterns](references/patterns.md). Xem [examples](references/examples.md) để phân biệt sửa hợp lý với over-editing.

## Anti-goals

- Không tuyên bố đoạn văn do AI viết hoặc chấm "xác suất AI".
- Không hỗ trợ vượt detector, thêm lỗi, tiếng lóng hay chi tiết giả.
- Không áp một giọng thân mật cho mọi văn bản.
- Không làm phẳng khác biệt vùng miền, thế hệ hoặc nghề nghiệp.
- Không rút gọn nội dung quan trọng chỉ để câu ngắn hơn.
- Không thay từ đồng nghĩa hàng loạt khi cấu trúc mới là vấn đề.
- Không biến nội dung kỹ thuật, học thuật hoặc pháp lý thành bản quảng cáo.

## Cách chọn mức can thiệp

Không mặc định mọi câu có tín hiệu đều phải sửa. Chọn một mức:

- **Giữ nguyên**: câu đã đúng nghĩa và register, hoặc tín hiệu catalog không đủ chắc.
- **Viết lại**: có thể sửa cấu trúc hoặc lỗi mà không đổi dữ kiện, lập trường hay thuật ngữ.
- **Góp ý**: cần người viết xem lại; nêu vị trí và lựa chọn, đừng tự đoán.
- **Cần tác giả quyết định**: xưng hô, glossary, hoặc cách hiểu làm đổi nghĩa.

## Đầu ra

Mặc định chỉ trả bản đã biên tập. Không thêm lời dẫn như “Dưới đây là phiên bản…” hay “Nếu bạn cần, tôi có thể…”. Khi người dùng yêu cầu review, dùng [review template](assets/review-template.md) và [rubric](references/evaluation.md). Không gắn nhãn chắc chắn cho tác giả hay nguồn gốc văn bản.
