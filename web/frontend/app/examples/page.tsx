import type { Metadata } from "next";
import Link from "next/link";
import { ReadingHeader } from "../../components/ReadingLayout";
import styles from "../../components/ReadingLayout.module.css";
import { ComparisonExplorer } from "../../components/ComparisonExplorer";
import { ABReviewEntry } from "../../components/ABReview";
import comparisons from "../../content/comparisons.json";
import { REPOSITORY_URL } from "../../lib/repository";

export const metadata: Metadata = {
  title: "Ví dụ biên tập",
  description:
    "Đọc sáu cặp bản sửa nguyên văn từ các lượt chạy AI. Mỗi cặp có cùng đoạn gốc, yêu cầu và bản ghi để đối chiếu.",
  alternates: { canonical: "/examples" },
};

export default function ExamplesPage() {
  return (
    <div className={styles.examples}>
      <ReadingHeader title="Câu chữ thay đổi ra sao?">
        Đọc hai bản sửa từ cùng một bản nháp. Một lượt AI dùng thêm bộ hướng dẫn
        tiếng Việt. Sáu cặp này minh họa cách sửa ở từng đề bài.
      </ReadingHeader>
      <ComparisonExplorer
        cases={comparisons.cases}
        initialId="technical"
        headingLevel={2}
      />
      <details className={styles.methodology}>
        <summary>Cách tạo sáu cặp ví dụ</summary>
        <p>
          Ngày 04/11/2026, hai agent Codex nhận cùng sáu đoạn giả định và yêu
          cầu biên tập. Một agent chỉ đọc đề bài. Agent kia đọc thêm
          humanizer-vi và tài liệu theo loại bài tại commit <code>845c379</code>
          . Cả sáu cặp được đăng nguyên văn.
        </p>
        <p>
          Hai agent dùng chung chỉ dẫn của môi trường Codex. Model được kế thừa
          từ phiên làm việc. Bản ghi thiếu mã phiên bản của nhà cung cấp và
          seed. Các ví dụ này chưa qua chấm độc lập của người đọc.
        </p>
        <p>
          Bạn có thể xem đầy đủ đề bài, đoạn gốc, kết quả và mã băm của tệp
          nguồn trong{" "}
          <a
            className="text-link"
            href={REPOSITORY_URL + "/tree/main/" + comparisons.sourceDirectory}
            target="_blank"
            rel="noopener noreferrer"
          >
            bản ghi trên GitHub
          </a>
          .
        </p>
      </details>
      <ABReviewEntry />
      <section className={styles.nextAction} aria-labelledby="examples-next">
        <div>
          <h2 id="examples-next">Thử với bản nháp của bạn</h2>
          <p>Dán văn bản vào trình soát hoặc lấy yêu cầu mẫu cho chatbot.</p>
        </div>
        <div className={styles.actions}>
          <Link className="button-primary" href="/check">
            Soát văn bản
          </Link>
          <Link className="button-secondary" href="/start">
            Dùng trong chatbot
          </Link>
        </div>
      </section>
    </div>
  );
}
