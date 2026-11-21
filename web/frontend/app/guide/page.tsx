import type { Metadata } from "next";
import Link from "next/link";
import { ReadingLayout } from "../../components/ReadingLayout";
import { InstallCommand } from "../../components/InstallCommand";

export const metadata: Metadata = {
  title: "Hướng dẫn sử dụng",
  description:
    "Cách soát văn bản trên web, chọn giọng và cung cấp ngữ cảnh khi biên tập bằng chatbot hoặc AI agent.",
  alternates: { canonical: "/guide" },
};

export default function GuidePage() {
  return (
    <ReadingLayout
      title="Từ bản nháp đến bản sửa"
      introduction="Cách chọn nhóm kiểm tra, đưa ngữ cảnh cho chatbot và đọc gợi ý trước khi sửa."
      contentsLabel="Mục lục hướng dẫn"
      contents={[
        { href: "#on-web", label: "Soát trên web" },
        { href: "#chatbot", label: "Dùng trong chatbot" },
        { href: "#context", label: "Thêm ngữ cảnh" },
        { href: "#review", label: "Đọc gợi ý" },
        { href: "#agent", label: "Cài cho AI agent" },
      ]}
    >
      <section id="on-web">
        <h2>Soát văn bản trên web</h2>
        <ol>
          <li>
            Mở <Link href="/check">trình soát</Link> và dán đoạn cần xem. Bạn
            cũng có thể thử văn bản mẫu.
          </li>
          <li>
            Chọn nhóm phù hợp với việc cần làm, như soát lỗi tiếng Việt hoặc sửa
            câu dịch chưa tự nhiên.
          </li>
          <li>
            Bấm “Soát văn phong”. Mỗi phát hiện ghi vị trí, lý do và gợi ý.
          </li>
          <li>
            Đọc cả đoạn trước khi áp dụng gợi ý. Kiểm tra lại sau khi chỉnh nếu
            còn chỗ cần xem.
          </li>
        </ol>
        <Link href="/check" className="button-primary">
          Soát văn bản
        </Link>
      </section>
      <section id="chatbot">
        <h2>Dùng trong chatbot</h2>
        <p>
          Vào trang <Link href="/start">Dùng trong chatbot</Link> và chọn công
          cụ bạn đang dùng. Với Claude hoặc Gemini, trang có gói tải và các bước
          cài. Với ChatGPT hoặc chatbot khác, bạn có thể lấy yêu cầu mẫu.
        </p>
        <p>
          Nếu chatbot đọc được tệp, tải bộ hướng dẫn đầy đủ rồi đính kèm khi gửi
          văn bản. Nói rõ phần hướng dẫn bạn muốn dùng và kết quả cần nhận.
        </p>
      </section>
      <section id="context">
        <h2>Cho biết bạn đang viết cho ai</h2>
        <p>
          Nêu loại bài, người đọc và những chi tiết phải giữ. Một email gửi đồng
          nghiệp cần ngữ cảnh khác một bài chia sẻ với bạn bè.
        </p>
        <div className="prose-note">
          <p>
            “Sửa nhẹ email này để gửi đồng nghiệp. Giữ cách xưng hô mình–bạn,
            thời hạn và trạng thái các việc chưa được duyệt. Có thể gộp câu. Trả
            lại email đã sửa.”
          </p>
        </div>
        <p>
          Chọn loại bài theo mục đích, từ văn viết phổ thông, công việc và kỹ
          thuật đến hành chính, mạng xã hội và marketing. Sau đó chọn riêng
          kênh, mức trang trọng, xưng hô và mức sửa.
        </p>
        <p>
          Với văn bản theo mẫu cơ quan, gửi kèm mẫu nếu có. Với bài quảng cáo,
          cung cấp giá, điều kiện và những lợi ích đã xác nhận.
        </p>
      </section>
      <section id="review">
        <h2>Đọc từng loại gợi ý</h2>
        <ul>
          <li>
            <strong>Lỗi cần sửa.</strong> Xem chỗ được đánh dấu để kiểm tra
            chính tả, ngữ pháp hoặc định dạng.
          </li>
          <li>
            <strong>Cần xem lại.</strong> Đọc cả câu trước và sau rồi quyết định
            có nên chỉnh.
          </li>
          <li>
            <strong>Lựa chọn cách viết.</strong> Cân nhắc giọng, người đọc và
            quy ước của bài.
          </li>
          <li>
            <strong>Tín hiệu tham khảo.</strong> Rà lại xem cấu trúc đang dùng
            có hợp ngữ cảnh không.
          </li>
        </ul>
        <p>
          Khi có tính năng viết lại bằng AI, kết quả có thể là bản sửa, bản giữ
          nguyên, nhận xét cần kiểm chứng hoặc câu hỏi cho bạn. Đối chiếu số
          liệu, điều kiện, phủ định và mức chắc chắn với bản gốc trước khi dùng.
        </p>
        <p>
          Nếu kết quả trống, các quy tắc đã chọn chưa tìm thấy chỗ cần lưu ý.
          Đọc lại các thông tin quan trọng trước khi gửi hoặc đăng.
        </p>
      </section>
      <section id="agent">
        <h2>Cài bộ skill cho AI agent</h2>
        <p>
          Chạy lệnh dưới đây trong terminal của dự án. Khi gửi văn bản, yêu cầu
          agent dùng skill phù hợp với việc cần làm.
        </p>
        <InstallCommand />
        <p>
          Xem <Link href="/examples">các cặp ví dụ biên tập</Link> để đọc hai
          cách sửa cùng một bản nháp.
        </p>
      </section>
    </ReadingLayout>
  );
}
