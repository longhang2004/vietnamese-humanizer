import Link from "next/link";
import { REPOSITORY_URL } from "../lib/repository";

export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="footer-grid">
        <div className="footer-brand">
          <h2>Vietnamese Writing Skills</h2>
          <p>
            Soát văn bản trên web. Dùng bộ hướng dẫn với chatbot hoặc AI agent.
          </p>
        </div>
        <div>
          <h2>Công cụ</h2>
          <ul>
            <li>
              <Link href="/check">Soát văn bản</Link>
            </li>
            <li>
              <Link href="/start">Dùng trong chatbot</Link>
            </li>
            <li>
              <Link href="/examples">Ví dụ biên tập</Link>
            </li>
            <li>
              <Link href="/guide">Hướng dẫn</Link>
            </li>
          </ul>
        </div>
        <div>
          <h2>Dự án</h2>
          <ul>
            <li>
              <Link href="/about">Về dự án</Link>
            </li>
            <li>
              <a
                href={REPOSITORY_URL}
                target="_blank"
                rel="noopener noreferrer"
              >
                Mã nguồn trên GitHub
              </a>
            </li>
            <li>
              <a
                href={REPOSITORY_URL + "/releases"}
                target="_blank"
                rel="noopener noreferrer"
              >
                Các bản phát hành
              </a>
            </li>
            <li>
              <a
                href={REPOSITORY_URL + "/issues"}
                target="_blank"
                rel="noopener noreferrer"
              >
                Góp ý và báo lỗi
              </a>
            </li>
          </ul>
        </div>
      </div>
      <div className="footer-bottom">
        <span>
          Mã nguồn mở ·{" "}
          <a className="text-link" href={REPOSITORY_URL + "/blob/main/LICENSE"}>
            Giấy phép MIT
          </a>
        </span>
      </div>
    </footer>
  );
}
