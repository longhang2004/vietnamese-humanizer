import type { Metadata } from "next";
import Link from "next/link";
import { ReadingHeader } from "../../components/ReadingLayout";
import styles from "../../components/ReadingLayout.module.css";
import { ComparisonExplorer } from "../../components/ComparisonExplorer";
import comparisons from "../../content/comparisons.json";
import { REPOSITORY_URL } from "../../lib/repository";

export const metadata: Metadata = {
  title: "Ví dụ AI có và không nạp skill",
  description:
    "Đối chiếu sáu cặp kết quả biên tập AI chạy thật, cùng yêu cầu, đoạn gốc và bản ghi có nguồn.",
  alternates: { canonical: "/examples" },
};

export default function ExamplesPage() {
  return (
    <div className={styles.examples}>
      <ReadingHeader title="Khi AI có thêm bộ skill tiếng Việt.">
        Cùng đoạn gốc và yêu cầu biên tập, hai agent xử lý trong hai ngữ cảnh
        riêng. Chọn một chủ đề để đọc cả hai bản.
      </ReadingHeader>
      <ComparisonExplorer
        cases={comparisons.cases}
        initialId="technical"
        headingLevel={2}
      />
      <details className={styles.methodology}>
        <summary>Các ví dụ được tạo như thế nào?</summary>
        <p>
          Ngày 04/11/2026, hai Codex subagent nhận cùng sáu đoạn giả định và yêu
          cầu biên tập. Một agent chỉ đọc đề bài; agent còn lại đọc thêm
          humanizer-vi và các tài liệu theo loại bài tại commit{" "}
          <code>845c379</code>. Cả sáu cặp được xuất lên web nguyên văn, không
          sửa lại để tạo khác biệt.
        </p>
        <p>
          Hai bên đều chịu chỉ dẫn chung của môi trường Codex. Model được kế
          thừa từ phiên làm việc; công cụ không công bố mã phiên bản provider
          hoặc seed. Vì vậy đây là ví dụ minh họa từng lượt chạy, chưa phải phép
          đo chất lượng chung hoặc đánh giá độc lập bằng người thật.
        </p>
        <p>
          Một số cặp chỉ khác vài chữ. Bạn có thể xem toàn bộ yêu cầu, đoạn gốc,
          đầu ra và hash nguồn trong{" "}
          <a
            className="text-link"
            href={REPOSITORY_URL + "/tree/main/" + comparisons.sourceDirectory}
            target="_blank"
            rel="noopener noreferrer"
          >
            bản ghi gốc
          </a>
          .
        </p>
      </details>
      <section className={styles.nextAction} aria-labelledby="examples-next">
        <div>
          <h2 id="examples-next">Thử với đoạn của bạn.</h2>
          <p>Soát ngay trên web, hoặc chọn skill cho chatbot.</p>
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
