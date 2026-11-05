import Link from "next/link";
import { ComparisonExplorer } from "../components/ComparisonExplorer";
import { Icon } from "../components/Icon";
import { InstallCommand } from "../components/InstallCommand";
import comparisons from "../content/comparisons.json";
import { starterSkills } from "../lib/onboarding";
import { REPOSITORY_URL } from "../lib/repository";

export default function HomePage() {
  return (
    <>
      <section className="home-intro" aria-labelledby="home-title">
        <h1 id="home-title">
          Tiếng Việt,
          <br />
          <span>đúng ý mình.</span>
        </h1>
        <div className="home-summary">
          <p>
            Biên tập câu chữ, soát lỗi và giữ cách viết nhất quán. Dùng ngay
            trên web hoặc thêm vào chatbot bạn đang dùng.
          </p>
          <div className="home-actions">
            <Link href="/check" className="button-primary">
              Kiểm tra văn bản <Icon name="arrow" width="18" height="18" />
            </Link>
            <Link href="/start" className="button-secondary">
              Dùng trong chatbot
            </Link>
          </div>
        </div>
      </section>

      <section
        id="comparison"
        className="proof-section"
        aria-labelledby="comparison-title"
      >
        <header className="section-heading">
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
        </header>
        <ComparisonExplorer cases={comparisons.cases} initialId="technical" />
        <div className="proof-end">
          <p>6 chủ đề, từ email công việc đến chia sẻ đời thường.</p>
          <Link href="/examples" className="text-link action-link">
            Xem cách chạy và các ví dụ{" "}
            <Icon name="arrow" width="16" height="16" />
          </Link>
        </div>
      </section>

      <section
        className="home-capabilities"
        aria-labelledby="capabilities-title"
      >
        <div>
          <h2 id="capabilities-title">
            Chọn đúng chỗ
            <br />
            cần sửa.
          </h2>
          <p className="section-description">
            Chỉnh văn phong, sửa câu dịch hay soát lỗi đều có tiêu chí riêng.
            Bốn skill giúp bạn tập trung vào việc đang cần.
          </p>
        </div>
        <dl className="capability-list">
          {starterSkills.map((skill) => (
            <div className="capability-row" key={skill.id}>
              <dt>{skill.title}</dt>
              <dd>
                <p>{skill.summary}</p>
                <code>{skill.id}</code>
              </dd>
            </div>
          ))}
        </dl>
      </section>

      <section className="use-section" aria-labelledby="use-title">
        <h2 id="use-title">Bắt đầu từ công cụ bạn đang dùng.</h2>
        <div className="use-row">
          <h3>Soát ngay trên web</h3>
          <p>
            Dán đoạn cần kiểm tra, chọn nhóm quy tắc và đọc gợi ý theo từng vị
            trí.
          </p>
          <Link href="/check" className="text-link action-link">
            Mở trình soát <Icon name="arrow" width="16" height="16" />
          </Link>
        </div>
        <div className="use-row">
          <h3>Dùng trong chatbot</h3>
          <p>
            Chọn ChatGPT, Claude, Gemini hoặc chatbot khác. Tải skill, đính kèm
            tài liệu hoặc sao chép yêu cầu mẫu theo hướng dẫn.
          </p>
          <Link href="/start" className="text-link action-link">
            Chọn chatbot <Icon name="arrow" width="16" height="16" />
          </Link>
        </div>
        <div className="use-row use-row-install">
          <div>
            <h3>Thêm vào AI agent</h3>
            <a
              href={REPOSITORY_URL + "/blob/main/README.md"}
              className="text-link action-link mt-3 text-sm"
              target="_blank"
              rel="noopener noreferrer"
            >
              Tài liệu trong repo{" "}
              <Icon name="external" width="15" height="15" />
            </a>
          </div>
          <InstallCommand />
        </div>
      </section>

      <section className="faq-section" aria-labelledby="faq-title">
        <div className="faq-heading">
          <h2 id="faq-title">Câu hỏi thường gặp</h2>
          <p>
            <Link href="/guide" className="text-link action-link">
              Đọc hướng dẫn sử dụng <Icon name="arrow" width="16" height="16" />
            </Link>
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
              Có. Hai Codex subagent nhận cùng sáu đề bài; một agent nạp thêm bộ
              skill tiếng Việt. Đầu ra được giữ nguyên văn, kèm yêu cầu, đoạn
              gốc và bản ghi để đối chiếu.
            </p>
          </details>
          <details>
            <summary>Tôi có thể góp ý hoặc bổ sung ví dụ không?</summary>
            <p>
              Bạn có thể gửi góp ý hoặc báo lỗi trong{" "}
              <a
                className="text-link"
                href={REPOSITORY_URL + "/issues"}
                target="_blank"
                rel="noopener noreferrer"
              >
                issue trên GitHub
              </a>
              . Mẫu đóng góp sẽ được nhóm duy trì xem xét trước khi thêm vào bộ
              dữ liệu.
            </p>
          </details>
        </div>
      </section>
    </>
  );
}
