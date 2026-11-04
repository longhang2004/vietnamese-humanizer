import Link from "next/link";
import { ComparisonExplorer } from "../components/ComparisonExplorer";
import { Icon } from "../components/Icon";
import { InstallCommand } from "../components/InstallCommand";
import comparisons from "../content/comparisons.json";
import { starterSkills } from "../lib/onboarding";
import { REPOSITORY_URL } from "../lib/repository";

export default function HomePage() {
  const example = comparisons.cases.find((item) => item.id === "technical")!;
  return (
    <>
      <section className="hero" aria-labelledby="home-title">
        <div className="hero-copy">
          <h1 id="home-title">
            Tiếng Việt,
            <br />
            <span>đúng ý mình.</span>
          </h1>
          <p>
            Biên tập câu chữ, soát lỗi và giữ cách viết nhất quán. Dùng ngay
            trên web hoặc thêm vào chatbot bạn đang dùng.
          </p>
          <div className="hero-actions">
            <Link href="/check" className="button-primary">
              Kiểm tra văn bản <Icon name="arrow" width="18" height="18" />
            </Link>
            <Link href="/start" className="button-secondary">
              Dùng trong chatbot
            </Link>
          </div>
          <InstallCommand />
        </div>
        <div className="hero-document">
          <div className="document-topline">
            <span>Ví dụ: Hướng dẫn thao tác</span>
            <code>humanizer-vi</code>
          </div>
          <div className="document-body">
            <div className="document-original">
              <h2>Một câu trong bản gốc</h2>
              <p>
                Để thực hiện việc nhập danh sách, bạn cần tiến hành bấm nút
                “Nhập CSV”, sau đó thực hiện việc chọn tệp .csv không quá 2 MB.
              </p>
            </div>
            <div className="document-result">
              <h2>
                <Icon name="book" width="16" height="16" />
                AI có nạp skill
              </h2>
              <p>{example.with}</p>
            </div>
          </div>
          <div className="document-footer">
            <span>Từ lượt chạy AI đã lưu</span>
            <a href="#comparison">
              So sánh hai bản <Icon name="arrow" width="14" height="14" />
            </a>
          </div>
        </div>
      </section>
      <div className="project-strip">
        <span>
          <Icon name="check" width="16" height="16" />4 skill tiếng Việt
        </span>
        <span>ChatGPT · Claude · Gemini · AI agent</span>
        <span>Mã nguồn mở · MIT</span>
        <a href={REPOSITORY_URL} target="_blank" rel="noopener noreferrer">
          Khám phá repo <Icon name="external" width="15" height="15" />
        </a>
      </div>
      <section
        id="comparison"
        className="section-space"
        aria-labelledby="comparison-title"
      >
        <div className="section-heading">
          <h2 id="comparison-title">
            Cùng một đoạn.
            <br />
            Hai cách biên tập.
          </h2>
          <p>
            Hai agent nhận cùng yêu cầu và đoạn gốc. Một bên nạp bộ skill tiếng
            Việt, bên còn lại biên tập theo cách thông thường. Bạn tự đối chiếu
            từng kết quả.
          </p>
        </div>
        <ComparisonExplorer cases={comparisons.cases} initialId="technical" />
        <div className="mt-6 flex flex-wrap items-center justify-between gap-4">
          <p className="text-sm text-[var(--muted)]">
            6 chủ đề, từ email công việc đến chia sẻ đời thường.
          </p>
          <Link href="/examples" className="text-link text-sm">
            Xem cách chạy và các ví dụ
          </Link>
        </div>
      </section>
      <section className="section-space features-layout">
        <div className="feature-intro">
          <h2>
            Chọn đúng chỗ
            <br />
            cần sửa.
          </h2>
          <p>
            Chỉnh văn phong, sửa câu dịch hay soát lỗi đều có tiêu chí riêng.
            Bốn skill giúp bạn tập trung vào việc đang cần.
          </p>
          <Link href="/check" className="text-link">
            Thử trên văn bản của bạn
          </Link>
        </div>
        <dl className="feature-list">
          {starterSkills.map((skill) => (
            <div className="feature-row" key={skill.id}>
              <dt>{skill.title}</dt>
              <dd>
                {skill.summary}
                <code>{skill.id}</code>
              </dd>
            </div>
          ))}
        </dl>
      </section>
      <section
        className="section-space choose-path"
        aria-label="Chọn cách sử dụng"
      >
        <div>
          <h2>
            Bắt đầu từ công cụ
            <br />
            bạn đang dùng.
          </h2>
          <p>
            Chọn ChatGPT, Claude, Gemini hoặc chatbot khác. Tải skill, đính kèm
            tài liệu hoặc sao chép yêu cầu mẫu theo hướng dẫn.
          </p>
          <Link href="/start" className="button-primary">
            Chọn chatbot <Icon name="arrow" width="17" height="17" />
          </Link>
        </div>
        <div>
          <h3>Thêm vào AI agent</h3>
          <p>
            Cài bộ skill từ repo và dùng trong quy trình viết, dịch hoặc review
            nội dung của bạn.
          </p>
          <InstallCommand />
          <a
            href={REPOSITORY_URL + "/blob/main/README.md"}
            className="text-link text-sm"
            target="_blank"
            rel="noopener noreferrer"
          >
            Xem tài liệu trong repo
          </a>
        </div>
      </section>
      <section
        className="section-space faq-section"
        aria-labelledby="faq-title"
      >
        <div className="feature-intro">
          <h2 id="faq-title">
            Bạn có thể
            <br />
            đang muốn biết.
          </h2>
          <p>
            <Link href="/guide" className="text-link">
              Đọc hướng dẫn sử dụng
            </Link>{" "}
            để chọn cách dùng phù hợp.
          </p>
        </div>
        <div className="faq-list">
          <details>
            <summary>Tôi dùng ngay trên web được không?</summary>
            <p>
              Được. Mở phần soát văn bản, dán nội dung và chọn những nhóm cần
              kiểm tra. Mỗi phát hiện có vị trí, lý do và gợi ý để bạn cân nhắc.
            </p>
          </details>
          <details>
            <summary>Skill dùng được với chatbot nào?</summary>
            <p>
              Có gói tải cho Claude và Gemini, cùng yêu cầu mẫu và tài liệu để
              dùng với ChatGPT hoặc chatbot khác. Trang bắt đầu sẽ chỉ cách phù
              hợp với công cụ bạn chọn.
            </p>
          </details>
          <details>
            <summary>Ví dụ so sánh có phải do AI tạo thật?</summary>
            <p>
              Có. Hai agent chạy trong hai ngữ cảnh riêng với cùng yêu cầu và
              đoạn gốc. Cả sáu cặp đầu ra được giữ nguyên văn; bản ghi và các
              tài liệu đã nạp được liên kết ngay dưới ví dụ.
            </p>
          </details>
          <details>
            <summary>Tôi có thể góp ý hoặc bổ sung ví dụ không?</summary>
            <p>
              Bạn có thể mở issue trên GitHub, mô tả đoạn văn, ngữ cảnh và điều
              cần xem lại. Nếu gửi ví dụ, hãy chọn nội dung bạn có quyền chia
              sẻ.
            </p>
          </details>
        </div>
      </section>
    </>
  );
}
