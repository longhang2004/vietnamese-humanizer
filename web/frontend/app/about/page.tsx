import type { Metadata } from "next";
import Link from "next/link";
import { ReadingLayout } from "../../components/ReadingLayout";
import { REPOSITORY_URL } from "../../lib/repository";

export const metadata: Metadata = {
  title: "Về dự án",
  description:
    "Tìm hiểu Vietnamese Writing Skills, nguồn xây dựng bộ hướng dẫn, cách kiểm chứng và cách đóng góp.",
  alternates: { canonical: "/about" },
};

export default function AboutPage() {
  return (
    <ReadingLayout
      title="Vietnamese Writing Skills"
      introduction="Bộ công cụ mã nguồn mở để soát và biên tập tiếng Việt theo ngữ cảnh."
      contentsLabel="Mục lục về dự án"
      contents={[
        { href: "#purpose", label: "Cách biên tập" },
        { href: "#coverage", label: "Công cụ và phạm vi" },
        { href: "#evidence", label: "Nguồn và kiểm chứng" },
        { href: "#contribute", label: "Góp ví dụ" },
      ]}
    >
      <section id="purpose">
        <h2>Sửa theo người đọc và mục đích</h2>
        <p>
          Một email công việc và một đoạn kể với bạn bè có thể cần hai cách sửa.
          Bộ hướng dẫn xét người đọc và tình huống trước khi chọn câu cần chỉnh.
        </p>
        <p>
          Khi câu đã rõ, có thể giữ nguyên. Khi cần sửa, những dữ kiện, cách
          xưng hô, lập trường và mức chắc chắn của tác giả vẫn phải đọc ra được.
        </p>
      </section>
      <section id="coverage">
        <h2>Công cụ và phạm vi</h2>
        <p>
          Trình soát web đánh dấu câu chữ theo quy tắc. Bộ skill hướng dẫn AI
          biên tập cả đoạn. Tính năng viết lại và góp mẫu trên web xuất hiện tùy
          cấu hình dịch vụ.
        </p>
        <p>
          Hệ thống hiện có 4 skill, 44 quy tắc, 103 ví dụ và 161 ca kiểm thử
          biên tập. Các loại bài gồm văn viết phổ thông, công việc, kỹ thuật,
          hành chính, mạng xã hội và marketing.
        </p>
        <p>
          Các phát hiện dùng để rà câu chữ. Chúng không xác định ai viết văn
          bản, chấm xác suất dùng AI hay kết luận gian lận.
        </p>
      </section>
      <section id="evidence">
        <h2>Nguồn đọc và kiểm chứng</h2>
        <p>
          Bộ hướng dẫn dựa trên bài viết tiếng Việt có nguồn, tài liệu chính
          thức và hướng dẫn biên tập. Dự án tự soạn ví dụ và ghi rõ những gì mỗi
          bản sửa cần giữ.
        </p>
        <p>
          <Link href="/examples">Trang ví dụ</Link> đăng nguyên văn kết quả AI
          và có bản ghi để đối chiếu. Bộ ca kiểm thử chưa có kết quả chuẩn đối
          chiếu do người bản ngữ chấm độc lập.
        </p>
        <p>
          Đọc thêm{" "}
          <a href={REPOSITORY_URL + "/tree/main/docs/research"}>
            nhật ký nghiên cứu
          </a>
          ,{" "}
          <a href={REPOSITORY_URL + "/blob/main/docs/limitations.md"}>
            giới hạn của công cụ
          </a>{" "}
          và <a href={REPOSITORY_URL + "/releases"}>các bản phát hành</a> trên
          GitHub.
        </p>
      </section>
      <section id="contribute">
        <h2>Một câu nên giữ nguyên cũng là ví dụ tốt</h2>
        <p>
          Gặp chỗ công cụ gợi ý chưa hợp? Gửi một đoạn ngắn, cho biết bạn viết
          cho ai và vì sao câu đó nên giữ hoặc sửa. Chọn nội dung bạn có quyền
          chia sẻ và bỏ thông tin riêng tư trước khi đăng.
        </p>
        <p>
          Mã nguồn được phát hành theo{" "}
          <a href={REPOSITORY_URL + "/blob/main/LICENSE"}>giấy phép MIT</a>.
        </p>
        <a href={REPOSITORY_URL + "/issues"} className="button-primary">
          Góp ý trên GitHub
        </a>
      </section>
    </ReadingLayout>
  );
}
