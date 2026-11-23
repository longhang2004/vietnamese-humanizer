---
name: humanizer-vi
description: Biên tập tiếng Việt sáo, máy móc, đều nhịp hoặc lệch giọng để tự nhiên, rõ và hợp độc giả. Dùng khi chỉnh văn phong, bảo toàn giọng tác giả, hoặc biên tập chat và kịch bản nói theo yêu cầu. Không dùng để suy đoán tác giả, lách detector hay chỉ soát lỗi ngữ pháp.
license: MIT
metadata:
  language: vi
  version: "0.5.0"
---

# Humanizer tiếng Việt

Biên tập chất lượng viết theo người đọc và mục đích văn bản; không phân loại nguồn gốc hay chấm "xác suất AI". Một tín hiệu đơn lẻ chưa đủ để sửa — xét cụm tín hiệu trong toàn đoạn.

## Quy trình

### Pha 1 — Chẩn đoán & biên tập tự nhiên

1. **Đọc toàn đoạn và neo giọng:** Xác định loại bài, độc giả, mục đích, register và giọng gốc (xưng hô, độ dài câu, mức trực tiếp, thuật ngữ). Khi thiếu dữ kiện, suy ra từ văn bản và can thiệp nhẹ. Nếu có **đoạn mẫu giọng viết (`voice_sample`)**, rút 3–4 đặc điểm diễn đạt (cách xưng hô, nhịp ngắt câu, tỷ lệ Hán-Việt/khẩu ngữ, cách mở–kết) để bám theo — tuyệt đối không mượn dữ kiện từ đoạn mẫu.
2. **Lập biên bản bảo toàn trong suy luận:** Ghi nhận số liệu, mốc thời gian, tên riêng, điều kiện, phủ định, mức chắc chắn, lập trường, code, URL và thuật ngữ cần giữ nguyên.
3. **Sửa theo tầng đoạn → câu → từ:** Viết trực tiếp như người viết thật nói với đúng người nhận. Ưu tiên tháo câu vòng, danh hóa nặng, nhịp phẳng, lời dẫn thừa và giải thích chen ngang; giữ nguyên câu đã ổn. Viết theo việc người đọc đang cần: chỉ giữ hoặc đặt định nghĩa, điều kiện, cảnh báo và câu phân biệt tại đúng vị trí giúp họ hiểu hoặc thao tác.

### Pha 2 — Đối chiếu bảo toàn & rà sửa thừa

4. **Đọc bản sửa độc lập như người nhận:** Kiểm tra mạch câu có tự đứng vững, đại từ có tiền ngữ rõ, có rò giọng trợ lý hay rơi vào khuôn mẫu khác không. Trong bài kể, kiểm ai đang làm hoặc đang nhớ; trong hướng dẫn, kiểm dấu hiệu được đi tiếp nằm ngay tại bước liên quan.
5. **Đối chiếu biên bản bảo toàn với bản gốc:** Kiểm lại từng con số, mốc giờ, phủ định, từ chỉ mức chắc chắn (`có thể`, `sẽ`, `phải`, `chưa`), phạm vi và ngoại lệ. Nếu cách sửa làm đổi nghĩa hoặc thiếu căn cứ, hoàn nguyên hoặc chuyển sang góp ý / hỏi tác giả. Chỉ giải thích thay đổi khi người dùng yêu cầu.

### Tài liệu tra cứu theo nhu cầu

- Khi chỉnh văn phong: đọc [diễn đạt tự nhiên](references/naturalness.md).
- Văn bản dài hoặc nhiều pattern chồng nhau: đọc [workflow chi tiết](references/workflow.md).
- Văn bản học thuật, pháp lý, hành chính, chăm sóc khách hàng: tra [register](references/registers.md).
- Kênh chat hoặc kịch bản nói: đọc [hội thoại và kịch bản nói](references/conversational.md).
- Văn cợt nhả, tự trào hoặc trào phúng, châm biếm: đọc [văn cợt nhả và trào phúng](references/humor-and-satire.md).
- Bài lặp đối lập, câu tự nhấn ý, nhịp giật ngắn, chia nhỏ quá mức hoặc kết đoạn tóm lại: đọc [sửa lối viết theo khuôn](references/formulaic-prose.md).
- Khi người dùng chọn loại bài: đọc [writing profiles](references/writing-profiles.md) rồi chọn đúng một tài liệu: [văn viết rõ ràng](references/plain-writing.md), [trao đổi công việc](references/business-writing.md), [tài liệu kỹ thuật](references/technical-writing.md), [hành chính](references/administrative-writing.md), [bài đăng mạng xã hội](references/social-writing.md) hoặc [marketing](references/marketing-writing.md).

## Ngữ cảnh và quyền biên tập

- Tách biệt kênh (tài liệu, email, chat, kịch bản nói), người đọc, quan hệ giao tiếp, xưng hô và độ trang trọng. Chọn kênh chat không cho phép tự đổi "tôi" thành "em" hoặc thêm "ạ". Profile không tự đổi giọng, kênh, xưng hô hay mức can thiệp.
- Mặc định sửa nhẹ và giữ giọng gốc; chỉ sắp xếp lại đoạn khi người dùng cho phép can thiệp sâu.
- Khi người dùng bật giảm cường điệu (`reduce_hype=true`), có thể gọt tính từ quảng cáo hoặc lớp đồng cảm công thức, nhưng vẫn giữ nguyên số liệu, phạm vi, mức chắc chắn, nghĩa vụ và lập trường tích cực. Nếu bỏ một nhận định làm đổi thông điệp, góp ý để tác giả quyết định.

## Bảo toàn

- Giữ nguyên dữ kiện, con số, tên riêng, trích dẫn, điều kiện, ngoại lệ, lập trường, thuật ngữ và mức độ chắc chắn. Không đổi "có thể" thành "sẽ", không xóa giới hạn và không thêm ví dụ, trải nghiệm hay cơ chế chưa có.
- Trong báo cáo và bài nghiên cứu, đặt mốc chốt, phạm vi, điều kiện đo và nguồn sát kết quả. Phân biệt kết quả ghi nhận, diễn giải, kiến nghị và dự kiến; giữ đúng mức quan hệ tương quan hay ước tính (xem thêm phần báo cáo trong [tài liệu kỹ thuật](references/technical-writing.md)).
- Chỉ dùng thông tin ngoài đoạn gốc khi nó được nêu rõ trong context; tuyệt đối không lấy dữ kiện từ `voice_sample` và không viện dẫn "chi tiết đã có trong bài" nếu không nằm trong dữ liệu đầu vào.
- Khi một câu mơ hồ theo nhiều cách hợp lý làm đổi kết quả đáng kể, giữ nguyên hoặc hỏi lại. Kiểm tra theo checklist đầy đủ trong [preservation rules](references/preservation-rules.md).

## Cách chọn mức can thiệp và pattern

- Chọn một mức: **Giữ nguyên** (đã rõ và hợp giọng, hoặc tín hiệu yếu); **Viết lại** (sửa cấu trúc/lỗi mà không đổi nghĩa); **Góp ý** (thiếu bằng chứng hoặc nguồn); **Cần tác giả quyết định** (mơ hồ xưng hô, thuật ngữ, cách hiểu đổi nghĩa).
- Ưu tiên xử lý pattern làm mất thông tin hoặc lệch register; xét mật độ từ nối, lời mở, danh sách và nhịp câu trên cả đoạn. Không sửa một cụm chỉ vì nó nằm trong [patterns](references/patterns.md); chỉ giữ hoặc tăng cá tính khi bản gốc đã có cơ sở. Xem thêm [examples](references/examples.md) để tránh over-editing.

## Anti-goals

- Không tuyên bố văn bản do AI viết, chấm "xác suất AI" hay tối ưu để vượt detector.
- Không thêm lỗi, tiếng lóng giả, chi tiết bịa hoặc lời mời trợ lý ("Nếu bạn muốn, tôi có thể…") vào bản sửa.
- Không áp một giọng thân mật cho mọi văn bản, làm phẳng khác biệt vùng miền/thế hệ/nghề nghiệp, hay rút gọn làm mất ý quan trọng.
- Không thay từ đồng nghĩa hàng loạt khi cấu trúc mới là vấn đề, và không biến nội dung kỹ thuật, học thuật hoặc pháp lý thành văn quảng cáo.

## Đầu ra

Khi đủ căn cứ biên tập an toàn, mặc định chỉ trả bản đã sửa; nếu đoạn đã phù hợp, giữ nguyên. Khi cần kiểm chứng hoặc tác giả quyết định, chỉ trả nhận xét hoặc câu hỏi cụ thể và chờ xác nhận trước khi đưa bản thay thế. Không thêm lời dẫn trước/sau văn bản thay thế hay mang lưu ý nội bộ của skill vào bài viết. Khi người dùng yêu cầu chấm hoặc review, dùng [review template](assets/review-template.md) và [rubric](references/evaluation.md).
