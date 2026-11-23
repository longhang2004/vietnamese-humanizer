# Ghi chú khảo sát: Văn nói, văn cợt nhả và văn trào phúng

Ngày ghi nhận: 23-11-2026. Đợt khảo sát này tổng hợp đặc trưng ngôn ngữ cho ba nhóm sắc thái chưa được hướng dẫn sâu ở các bản trước: (1) văn nói có kịch bản hoặc bán tự phát (lời thoại phim, vlog, video kiến thức), (2) văn cợt nhả / tự trào trên mạng xã hội, và (3) văn trào phúng, châm biếm trong truyền thống văn học–báo chí Việt Nam.

Các tình huống kiểm chứng trong `benchmarks/cases/spoken-humor-satire.jsonl` đều là ví dụ giả định do agent tự soạn; chưa sao chép tác phẩm gốc hay dữ liệu mạng xã hội thật làm corpus, và chưa có đợt chấm độc lập bởi người bản ngữ.

---

## 1. Văn nói: lời thoại phim, vlog và video kiến thức

Khác với văn bản đọc thầm, văn nói hoạt động theo **tuyến tính thời gian** (người nghe không quét ngược đoạn văn) và gắn chặt với **tình huống giao tiếp trực tiếp**:

- **Lời thoại phim và tiểu phẩm:** sử dụng dày đặc phép **tỉnh lược tình huống** (bỏ chủ ngữ hoặc tân ngữ khi đồ vật/người đối diện nằm ngay trong cảnh), **bắt từ khóa lượt trước** (lặp một chữ từ câu hỏi hoặc mệnh lệnh của đối phương để phản bác hoặc hỏi vặn), và **tiểu từ tình thái cuối câu** (`đâu`, `đấy`, `chứ`, `cơ mà`, `hả`, `thôi`, `nha`, `nghen`) để định vị quan hệ xã hội lẫn thái độ người nói. Khi biên tập thoại, giữ lượt ngắt và khẩu ngữ đặc trưng của nhân vật thay vì kéo về câu chủ–vị đầy đủ kiểu biên bản.
- **Vlog và chia sẻ trước ống kính:** mở trực tiếp vào hành động bằng từ chỉ xuất (`đây`, `khúc này`, `hồi nãy`) thay cho câu thông báo meta (*"Trong video hôm nay, chúng ta sẽ cùng..."*); hay dùng **nhịp bồi cuối câu** (nêu ý chính trước rồi nối thêm chi tiết đính chính ngắn phía sau) và chuyển ý bằng hành động đang làm thay cho liên từ văn viết (`đồng thời`, `bên cạnh đó`).
- **Video kiến thức / explainer:** mỗi hơi thở giữ một mệnh đề rõ, ưu tiên mở từ điểm nghẽn thực tế rồi đặt khung Đề – Thuyết ngắn gọn; đổi tham chiếu mắt đọc (*"như biểu đồ phía trên"*) sang chỉ dẫn nghe/nhìn phù hợp lời dẫn nhưng vẫn bảo toàn nguyên vẹn giới hạn và mức chắc chắn của số liệu (`ước tính`, `trong mẫu thử`).

Phần vận dụng nằm tại [hội thoại và kịch bản nói](../../skills/humanizer-vi/references/conversational.md).

---

## 2. Văn cợt nhả, tự trào và giễu nhại mạng xã hội

Trong giao tiếp thân mật và bài đăng mạng xã hội tiếng Việt, giọng cợt nhả hoạt động nhờ sự **lệch pha có chủ đích** giữa nội dung đời thường và cách diễn đạt:

- **Tự trào phủ đầu (self-deprecation):** người viết tự nêu tình huống éo le, thiếu sót hoặc hết tiền bằng giọng bình thản để tự vô hiệu hóa lời chê từ ngoài, tránh tự an ủi hoặc giải thích dài dòng.
- **Nhại văn phong nghiêm trọng cho chuyện nhỏ (mock-formal):** mượn từ ngữ hành chính, hội đồng, tài chính hoặc khoa học để mô tả việc sinh hoạt vặt vãnh (*"hội đồng thẩm định dạ dày"*, *"cơ chế giải ngân lương"*).
- **Bẻ nhịp anti-climax:** dựng mệnh đề mở trang trọng hoặc hoành tráng rồi hạ xuống thực tế nhỏ nhặt ở cuối câu — điểm mấu chốt khi biên tập là **dừng ngay tại từ tạo twist**, tuyệt đối không thêm câu bình luận thừa kiểu *"đây quả là một tình huống dở khóc dở cười"*.

---

## 3. Văn trào phúng và châm biếm: tham chiếu từ *Số đỏ* (Vũ Trọng Phụng)

Tiểu thuyết *Số đỏ* (1936) của Vũ Trọng Phụng (cũng như mạch tiểu phẩm trào phúng báo chí tiếng Việt như mục Bút Bi đã ghi trong [danh mục văn phong](../style-catalog.md)) cho thấy bốn thủ pháp cốt lõi cần nhận diện đúng để không biên tập hỏng giọng tác giả:

1. **Nghịch ngữ (ghép hai cực đối lập giá trị):** tiêu biểu qua nhan đề và tình huống chương *"Hạnh phúc của một tang gia"* — đặt trang nghiêm/tang tóc cạnh hả hê/trưng diện. Trong văn bản thực tế (ví dụ châm biếm hội nghị *"tiết kiệm giấy"* nhưng in hàng trăm thư mời màu), mâu thuẫn được đặt thẳng cạnh nhau mà không cần người viết giảng giải thêm.
2. **Liệt kê đánh đồng bất tương xứng:** xếp những giá trị trang trọng ngang hàng với toan tính thực dụng trong cùng một chuỗi liệt kê, đặt chi tiết hạ bệ làm nốt chốt câu.
3. **Giọng kể giả vờ khách quan hoặc khen ngược (deadpan irony / mock-praise):** dùng từ ngữ ca ngợi quy củ (*"nhờ tinh thần quyết liệt..."*, *"thành tựu đáng kinh ngạc..."*) để thuật lại một kết quả ngược đời có thật trong dữ kiện. Nếu biên tập viên sửa câu khen ngược thành chê trực diện, toàn bộ hiệu ứng mỉa mai sẽ bị phá vỡ.
4. **Nhại chữ sáo và khẩu hiệu nửa mùa có chủ đích:** giống cách *Số đỏ* nhại lớp từ *"Âu hóa"*, *"văn minh"*, *"vui vẻ trẻ trung"* hoặc màn diễn thuyết công lý của Xuân Tóc Đỏ, bài châm biếm thường cố tình trích lại khẩu hiệu sáo để chế giễu chính khẩu hiệu đó. Người biên tập cần phân biệt **chữ sáo vô tình** (cần gọt) với **chữ sáo được mượn làm mồi châm biếm** (phải giữ từ khóa đó, chỉ tỉa các câu mở bài/giảng đạo lý thừa xung quanh).

Phần vận dụng và ranh giới bảo toàn (không cợt nhả trong thông báo sự cố/y tế/pháp lý; chuyển `review_comment` nếu bài châm biếm gán cáo buộc/số liệu thiếu nguồn) nằm tại [văn cợt nhả và trào phúng](../../skills/humanizer-vi/references/humor-and-satire.md).
