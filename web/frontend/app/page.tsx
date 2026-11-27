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
      <section className="home-stage" aria-labelledby="home-title">
        <div className="home-stage-lead">
          <h1 id="home-title">
            Sửa câu chữ.
            <br />
            <span>Giữ giọng riêng.</span>
          </h1>
          <div className="home-summary">
            <p>
              Soát lỗi tiếng Việt, tìm chỗ câu còn gượng và giữ cách viết nhất
              quán. Kiểm tra bản thảo trên web hoặc biên tập trong chatbot bạn
              quen dùng.
            </p>
            <div className="home-actions">
              <Link href="/check" className="button-primary">
                Soát văn bản <Icon name="arrow" width="18" height="18" />
              </Link>
              <Link href="/start" className="button-secondary">
                Dùng trong chatbot
              </Link>
            </div>
          </div>
          <div className="home-install">
            <InstallCommand variant="hero" label="Cài trực tiếp vào AI agent" />
          </div>
          <p className="home-facts">
            4 skill chuyên biệt · 49 quy tắc soát · 103 ví dụ có rà bảo toàn
          </p>
        </div>

        <div
          id="comparison"
          className="home-stage-specimen"
          aria-labelledby="comparison-title"
        >
          <header className="stage-specimen-head">
            <h2 id="comparison-title">Cùng một bản nháp. Hai bản sửa.</h2>
            <p>
              Hai lượt AI nhận cùng đoạn gốc và yêu cầu. Một lượt đọc thêm bộ
              hướng dẫn tiếng Việt. Chọn chủ đề để xem câu chữ thay đổi ra sao.
            </p>
          </header>
          <ComparisonExplorer cases={comparisons.cases} initialId="technical" />
          <div className="proof-end">
            <p>6 chủ đề, từ email công việc đến bài kể đời thường.</p>
            <Link href="/examples" className="text-link action-link">
              Xem ví dụ và bản ghi <Icon name="arrow" width="16" height="16" />
            </Link>
          </div>
        </div>
      </section>

      <section
        className="home-capabilities"
        aria-labelledby="capabilities-title"
      >
        <div>
          <h2 id="capabilities-title">Bạn muốn sửa chỗ nào?</h2>
          <p className="section-description">
            Bạn có thể dùng riêng từng bộ hướng dẫn theo việc cần làm.
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
        <div className="use-section-head">
          <h2 id="use-title">Chọn cách bắt đầu</h2>
          <p>
            Soát trực tiếp trên trình duyệt, lấy gói hướng dẫn cho chatbot hoặc
            cài vào agent dòng lệnh.
          </p>
        </div>
        <div className="use-layout">
          <article className="use-plate-primary">
            <h3>Trên web</h3>
            <p>
              Dán một đoạn văn trên tờ phiếu soạn thảo, chọn nhóm cần kiểm tra
              và xem từng vị trí được đánh dấu cùng gợi ý viết lại theo ngữ
              cảnh.
            </p>
            <Link href="/check" className="use-plate-action">
              Soát văn bản <Icon name="arrow" width="16" height="16" />
            </Link>
          </article>
          <div className="use-drawers">
            <article className="use-drawer">
              <h3>Trong chatbot</h3>
              <p>
                Tải skill cho Claude hoặc Gemini. Với ChatGPT hay chatbot khác,
                bạn có thể dùng yêu cầu mẫu hoặc đính kèm bộ hướng dẫn nếu có hỗ
                trợ.
              </p>
              <Link href="/start" className="text-link action-link">
                Chọn chatbot <Icon name="arrow" width="16" height="16" />
              </Link>
            </article>
            <article className="use-drawer">
              <div className="use-drawer-head">
                <h3>Trong AI agent</h3>
                <a
                  href={REPOSITORY_URL + "/blob/main/README.md"}
                  className="text-link action-link text-sm"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Xem cách cài trên GitHub{" "}
                  <Icon name="external" width="15" height="15" />
                </a>
              </div>
              <InstallCommand allowSkillSelect />
            </article>
          </div>
        </div>
      </section>

      <section className="faq-section" aria-labelledby="faq-title">
        <div className="faq-heading">
          <h2 id="faq-title">Câu hỏi thường gặp</h2>
          <p>
            <Link href="/guide" className="text-link action-link">
              Xem hướng dẫn <Icon name="arrow" width="16" height="16" />
            </Link>
          </p>
        </div>
        <div className="faq-list">
          <details>
            <summary>Tôi có thể thử ngay trên web không?</summary>
            <p>
              Có. Mở trình soát và dùng đoạn mẫu hoặc dán văn bản của bạn. Mỗi
              phát hiện ghi vị trí, lý do và gợi ý để bạn cân nhắc.
            </p>
          </details>
          <details>
            <summary>Nếu chatbot của tôi chưa có mục Skills?</summary>
            <p>
              Bạn vẫn có thể dán yêu cầu mẫu vào cuộc trò chuyện. Nếu chatbot hỗ
              trợ đọc tệp, hãy đính kèm bộ hướng dẫn đầy đủ.
            </p>
          </details>
          <details>
            <summary>Hai bản ví dụ được tạo ra sao?</summary>
            <p>
              Hai agent Codex chạy riêng trên cùng sáu đề bài. Một agent đọc
              thêm bộ hướng dẫn tiếng Việt. Bạn có thể đọc nguyên văn cả hai kết
              quả cùng đề bài và bản ghi của từng lượt.
            </p>
          </details>
          <details>
            <summary>Tôi có thể gửi góp ý ở đâu?</summary>
            <p>
              Mở{" "}
              <a
                className="text-link"
                href={REPOSITORY_URL + "/issues"}
                target="_blank"
                rel="noopener noreferrer"
              >
                một issue trên GitHub
              </a>{" "}
              để góp ý hoặc báo lỗi. Nhóm duy trì sẽ xem các ví dụ đóng góp
              trước khi đưa vào bộ dữ liệu.
            </p>
          </details>
        </div>
      </section>
    </>
  );
}
