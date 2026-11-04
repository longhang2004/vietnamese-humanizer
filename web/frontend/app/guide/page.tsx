import type { Metadata } from "next";
import Link from "next/link";
import { InstallCommand } from "../../components/InstallCommand";

export const metadata: Metadata = { title: "Hướng dẫn sử dụng", description: "Cách soát văn bản trên web, dùng skill trong chatbot và chọn loại bài, giọng, ngữ cảnh phù hợp.", alternates: { canonical: "/guide" } };

export default function GuidePage() {
  return <>
    <div className="page-heading"><h1>Bắt đầu với đoạn bạn muốn sửa.</h1><p>Chọn cách dùng, thêm ngữ cảnh cần thiết và đối chiếu gợi ý với bản gốc.</p></div>
    <div className="prose-layout">
      <nav className="guide-toc" aria-label="Mục lục hướng dẫn"><a href="#on-web">Soát trên web</a><a href="#chatbot">Dùng trong chatbot</a><a href="#context">Chọn giọng và ngữ cảnh</a><a href="#review">Đọc kết quả</a><a href="#agent">Dùng với AI agent</a></nav>
      <article className="prose-content">
        <section id="on-web"><h2>Soát văn bản trên web</h2><ol><li>Mở <Link href="/check">phần soát văn bản</Link>, rồi dán đoạn cần kiểm tra. Bạn có thể thử văn bản mẫu trước.</li><li>Chọn nhóm cần xem: văn phong tự nhiên, câu dịch, ngữ pháp hoặc tính nhất quán.</li><li>Bấm “Soát văn phong”. Đọc từng phát hiện cùng vị trí, lý do và gợi ý.</li><li>Chỉnh lại đoạn gốc theo điều bạn thấy phù hợp, rồi kiểm tra tiếp nếu cần.</li></ol><p>Công cụ dùng các quy tắc đã biên soạn để tìm chỗ cần xem lại. Một phát hiện về văn phong cần được xét trong cả đoạn và mục đích bài.</p><Link href="/check" className="button-primary">Mở trình soát</Link></section>
        <section id="chatbot"><h2>Dùng trong chatbot của bạn</h2><p>Vào <Link href="/start">trang bắt đầu</Link>, chọn ChatGPT, Claude, Gemini hoặc công cụ khác. Trang sẽ cung cấp gói tải và cách cài tương ứng, hoặc yêu cầu mẫu để sao chép.</p><p>Nếu chatbot hỗ trợ đính kèm tài liệu, bạn cũng có thể tải bộ hướng dẫn đầy đủ. Khi gửi văn bản, nói rõ phần cần áp dụng và kết quả bạn muốn nhận.</p></section>
        <section id="context"><h2>Chọn giọng và ngữ cảnh</h2><p>Bắt đầu bằng loại bài và người đọc. Ví dụ: email gửi đồng nghiệp, bài chia sẻ với bạn bè hay hướng dẫn cho người mới.</p><div className="prose-note"><p>“Biên tập email này để gửi đồng nghiệp. Giữ cách xưng hô mình–bạn, thời hạn và các việc chưa được duyệt. Có thể gộp câu, chỉ trả lại email đã sửa.”</p></div><p>Các loại bài hiện có: văn viết rõ ràng, trao đổi công việc, kỹ thuật, hành chính, bài đăng mạng xã hội và marketing. Kênh, mức trang trọng, cách xưng hô và mức sửa là những lựa chọn riêng.</p><p>Với văn bản hành chính, gửi kèm mẫu hoặc quy ước của đơn vị nếu có. Với marketing, cung cấp đủ giá, điều kiện và thông tin đã được xác nhận.</p></section>
        <section id="review"><h2>Đọc kết quả theo ngữ cảnh</h2><ul><li><strong>Lỗi cần sửa:</strong> kiểm tra chính tả, ngữ pháp hoặc hình thức tại vị trí được nêu.</li><li><strong>Cần xem lại:</strong> đọc câu cùng phần trước và sau để quyết định cách sửa.</li><li><strong>Lựa chọn cách viết:</strong> cân nhắc theo giọng, người đọc và quy ước riêng.</li><li><strong>Tín hiệu tham khảo:</strong> xem như một lời nhắc rà lại; cấu trúc đó vẫn có thể phù hợp.</li></ul><p>Khi tính năng viết lại bằng AI được bật, phần gợi ý có thể trả bản sửa, giữ nguyên, nhận xét cần kiểm chứng hoặc câu hỏi cho tác giả. Kiểm tra lại số liệu, điều kiện, phủ định và mức chắc chắn trước khi sử dụng.</p><p>Trường hợp không có phát hiện chỉ cho biết các quy tắc đã chọn chưa tìm ra chỗ cần lưu ý. Bạn vẫn nên đọc lại những nội dung quan trọng.</p></section>
        <section id="agent"><h2>Dùng với AI agent</h2><p>Trong terminal của dự án, chạy lệnh dưới đây để thêm bộ skill. Sau đó yêu cầu agent dùng skill phù hợp khi biên tập hoặc review nội dung.</p><InstallCommand /><p>Bạn có thể bắt đầu bằng một đoạn ngắn và xem <Link href="/examples">các ví dụ chạy thật</Link> để hiểu phạm vi hướng dẫn.</p></section>
      </article>
    </div>
  </>;
}
