import type { Metadata } from "next";
import Link from "next/link";
import { REPOSITORY_URL } from "../../lib/repository";

export const metadata: Metadata = {
  title: "Về dự án",
  description:
    "Mục đích, phạm vi và cách đóng góp cho Vietnamese Writing Skills.",
  alternates: { canonical: "/about" },
};

export default function AboutPage() {
  return (
    <>
      <div className="page-heading">
        <h1>Viết tiếng Việt, giữ giọng riêng.</h1>
        <p>
          Vietnamese Writing Skills là dự án mã nguồn mở về biên tập tiếng Việt
          theo ngữ cảnh.
        </p>
      </div>
      <div className="prose-layout">
        <nav className="guide-toc" aria-label="Mục lục về dự án">
          <a href="#purpose">Mục đích</a>
          <a href="#coverage">Phạm vi hiện tại</a>
          <a href="#evidence">Nguồn và kiểm chứng</a>
          <a href="#contribute">Đóng góp</a>
        </nav>
        <article className="prose-content">
          <section id="purpose">
            <h2>Câu rõ hơn, ý vẫn là của bạn.</h2>
            <p>
              Dự án tập trung vào bốn việc: chỉnh câu sáo hoặc lệch giọng, sửa
              lối diễn đạt bám cấu trúc dịch, soát lỗi tiếng Việt và giữ cách
              viết nhất quán.
            </p>
            <p>
              Cùng một nội dung có thể cần cách diễn đạt khác nhau tùy người
              đọc, mục đích và quan hệ giao tiếp. Bộ hướng dẫn ưu tiên giữ dữ
              kiện, lập trường, mức chắc chắn và cách xưng hô của tác giả.
            </p>
          </section>
          <section id="coverage">
            <h2>Phạm vi hiện tại</h2>
            <p>
              Bản 0.6.0 có bốn skill, 44 quy tắc rà soát, 103 ví dụ và 124 ca
              benchmark. Hướng dẫn theo loại bài gồm văn viết rõ ràng, công
              việc, kỹ thuật, hành chính, mạng xã hội và marketing.
            </p>
            <p>
              Trình soát web dùng quy tắc để tìm tín hiệu. Bộ skill cung cấp
              hướng dẫn cho AI biên tập cả đoạn. Tính năng viết lại và góp mẫu
              trên web phụ thuộc cấu hình dịch vụ.
            </p>
            <p>
              Dự án tập trung chất lượng văn bản. Các phát hiện không dùng để
              xác định một người có dùng AI, chấm xác suất tác giả hoặc kết luận
              gian lận.
            </p>
          </section>
          <section id="evidence">
            <h2>Nguồn đọc và kiểm chứng</h2>
            <p>
              Hướng dẫn được phát triển từ nguồn có quy thuộc rõ, gồm bài viết
              tiếng Việt, tài liệu chính thức và hướng dẫn biên tập. Ví dụ của
              dự án được tự viết, kèm điều cần giữ và giới hạn sử dụng.
            </p>
            <p>
              Bộ benchmark hiện chưa có baseline được người bản ngữ độc lập đánh
              giá. Các cặp AI trên <Link href="/examples">trang ví dụ</Link> là
              lượt chạy minh họa nguyên văn, có bản ghi nguồn và điều kiện sinh.
            </p>
            <p>
              Bạn có thể đọc{" "}
              <a href={REPOSITORY_URL + "/tree/main/docs/research"}>
                nhật ký nghiên cứu
              </a>
              ,{" "}
              <a href={REPOSITORY_URL + "/blob/main/docs/limitations.md"}>
                các giới hạn
              </a>{" "}
              và <a href={REPOSITORY_URL + "/releases"}>lịch sử phát hành</a>{" "}
              trong repo.
            </p>
          </section>
          <section id="contribute">
            <h2>Cùng bổ sung những trường hợp thật.</h2>
            <p>
              Nếu gặp một gợi ý chưa phù hợp, gửi đoạn ngắn đủ ngữ cảnh, loại
              bài, người đọc và lý do bạn muốn giữ hoặc sửa. Những phản ví dụ rõ
              ràng giúp dự án cải thiện các quy tắc.
            </p>
            <p>
              Chọn nội dung bạn có quyền chia sẻ và bỏ thông tin riêng tư trước
              khi gửi. Mã nguồn được phân phối theo{" "}
              <a href={REPOSITORY_URL + "/blob/main/LICENSE"}>giấy phép MIT</a>.
            </p>
            <a href={REPOSITORY_URL + "/issues"} className="button-primary">
              Góp ý trên GitHub
            </a>
          </section>
        </article>
      </div>
    </>
  );
}
