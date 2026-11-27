import type { Metadata } from "next";
import { GettingStarted } from "../../components/GettingStarted";
import { InstallCommand } from "../../components/InstallCommand";

export const metadata: Metadata = {
  title: "Dùng trong chatbot",
  description:
    "Chọn cách biên tập tiếng Việt trong ChatGPT, Claude, Gemini hoặc chatbot khác. Tải skill hoặc sao chép yêu cầu mẫu.",
  alternates: { canonical: "/start" },
};

export default function StartPage() {
  return (
    <>
      <GettingStarted />
      <section className="start-cli-band" aria-labelledby="start-cli-title">
        <div className="start-cli-copy">
          <h2 id="start-cli-title">Dùng trong AI agent dòng lệnh?</h2>
          <p>
            Cài nhanh vào Cursor, Claude Code, Codex, Antigravity hoặc Windsurf
            bằng một dòng lệnh <code>npx skills</code>.
          </p>
        </div>
        <InstallCommand allowSkillSelect />
      </section>
    </>
  );
}
