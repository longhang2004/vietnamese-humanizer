"use client";

import Link from "next/link";
import { useState } from "react";
import { Icon } from "./Icon";
import {
  chatgptInstallUrl,
  docsCheckedOn,
  Platform,
  skillDownload,
  starterPrompt,
  StarterScenarioId,
  starterScenarios,
  starterSkills,
} from "../lib/onboarding";
import styles from "./GettingStarted.module.css";

const PLATFORMS: { id: Platform; label: string; url: string }[] = [
  { id: "chatgpt", label: "ChatGPT", url: "https://chatgpt.com/" },
  { id: "claude", label: "Claude", url: "https://claude.ai/" },
  { id: "gemini", label: "Gemini", url: "https://gemini.google.com/" },
  { id: "other", label: "Chatbot khác", url: "" },
];

function CopyPrompt({ text }: { text: string }) {
  const [message, setMessage] = useState("");

  async function copy() {
    try {
      await navigator.clipboard.writeText(text);
      setMessage("Đã sao chép yêu cầu.");
    } catch {
      setMessage(
        "Chưa sao chép được. Chọn nội dung trong ô yêu cầu mẫu và sao chép trực tiếp.",
      );
    }
  }

  return (
    <div className={styles.copyPrompt}>
      <div className={styles.promptControls}>
        <label className={styles.promptLabel} htmlFor="starter-prompt">
          Yêu cầu mẫu
        </label>
        <button type="button" onClick={copy} className="button-primary">
          <Icon name="copy" width="16" height="16" />
          Sao chép yêu cầu
        </button>
      </div>
      <textarea
        id="starter-prompt"
        readOnly
        value={text}
        rows={10}
        className={`field ${styles.promptField}`}
      />
      <p role="status" className={styles.copyStatus}>
        {message}
      </p>
    </div>
  );
}

export function GettingStarted() {
  const [platformId, setPlatformId] = useState<Platform>("chatgpt");
  const [skillId, setSkillId] = useState(starterSkills[0].id);
  const [scenarioId, setScenarioId] = useState<StarterScenarioId>("default");
  const platform = PLATFORMS.find((item) => item.id === platformId)!;
  const skill = starterSkills.find((item) => item.id === skillId)!;
  const nativePlatform =
    platformId === "claude" || platformId === "gemini" ? platformId : null;
  const download = nativePlatform ? skillDownload(nativePlatform, skill) : null;

  return (
    <div className={styles.page}>
      <header className={`page-heading ${styles.header}`}>
        <div>
          <h1>Biên tập trong chatbot bạn quen dùng</h1>
          <p>Chọn chatbot để xem cách cài skill hoặc lấy yêu cầu mẫu.</p>
        </div>
        <Link href="/check" className="text-link action-link">
          Soát văn bản trên web
          <Icon name="arrow" width="16" height="16" />
        </Link>
      </header>

      <div className={styles.workspace}>
        <aside className={styles.choices} aria-label="Chatbot và việc cần làm">
          <fieldset>
            <legend>Bạn dùng chatbot nào?</legend>
            <div className={styles.platforms}>
              {PLATFORMS.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  aria-pressed={platformId === item.id}
                  onClick={() => setPlatformId(item.id)}
                  className={styles.platform}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </fieldset>

          <div className={styles.task}>
            <label htmlFor="starter-task">Việc cần làm</label>
            <select
              id="starter-task"
              value={skillId}
              onChange={(event) => setSkillId(event.target.value)}
              aria-describedby="starter-task-description"
              className="field"
            >
              {starterSkills.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.title}
                </option>
              ))}
            </select>
            <p id="starter-task-description">{skill.summary}</p>
            <label htmlFor="starter-scenario" className={styles.scenarioLabel}>
              Tình huống mẫu (tùy chọn)
            </label>
            <select
              id="starter-scenario"
              value={scenarioId}
              onChange={(event) =>
                setScenarioId(event.target.value as StarterScenarioId)
              }
              className="field"
            >
              {starterScenarios.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.label}
                </option>
              ))}
            </select>
          </div>
        </aside>

        <div className={styles.content}>
          <section className={styles.setup} aria-labelledby="starter-setup">
            <h2 id="starter-setup">Cách dùng với {platform.label}</h2>
            {download && (
              <div className={styles.nativeSetup}>
                <p>
                  Dùng gói ZIP nếu tài khoản có mục Skills. Khi chưa thấy mục
                  đó, bạn có thể lấy yêu cầu mẫu bên dưới.
                </p>
                <a href={download.href} download className="button-primary">
                  <span>Tải skill “{skill.title}”</span>
                  <span className={styles.downloadSize}>
                    ZIP · {download.size}
                  </span>
                </a>
                <ol>
                  <li>Tải tệp ZIP về máy.</li>
                  {platformId === "claude" ? (
                    <>
                      <li>
                        Trong Claude, vào Customize → Skills. Chọn thêm skill
                        rồi chọn Upload a skill và mở tệp vừa tải.
                      </li>
                      <li>
                        Bật skill sau khi tải lên. Nếu Claude yêu cầu, vào
                        Settings → Capabilities để bật Code execution and file
                        creation.
                      </li>
                    </>
                  ) : (
                    <>
                      <li>
                        Trong Gemini trên web, vào Customize → Skills → Create →
                        Upload. Chọn tệp ZIP vừa tải.
                      </li>
                      <li>Kiểm tra nội dung rồi bấm Create.</li>
                    </>
                  )}
                  <li>
                    Mở cuộc trò chuyện mới. Dán yêu cầu mẫu và thêm đoạn cần
                    biên tập.
                  </li>
                </ol>
              </div>
            )}
            {platformId === "chatgpt" && (
              <div className={styles.platformSetup}>
                {chatgptInstallUrl ? (
                  <a
                    href={chatgptInstallUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="button-primary"
                  >
                    Cài plugin trong ChatGPT
                  </a>
                ) : (
                  <p>
                    Plugin chưa có bản cài công khai. Bạn có thể sao chép yêu
                    cầu mẫu và dán vào cuộc trò chuyện mới.
                  </p>
                )}
              </div>
            )}
            {platformId === "other" && (
              <p className={styles.platformSetup}>
                Sao chép yêu cầu mẫu và dán vào cuộc trò chuyện mới trong
                chatbot bạn dùng.
              </p>
            )}
            {platform.url && (
              <a
                href={platform.url}
                target="_blank"
                rel="noopener noreferrer"
                className={`button-secondary ${styles.openPlatform}`}
              >
                Mở {platform.label}
                <Icon name="external" width="16" height="16" />
              </a>
            )}
          </section>

          <section className={styles.prompt} aria-labelledby="starter-try">
            <div className={styles.promptHeading}>
              <h2 id="starter-try">Gửi đoạn bạn cần sửa</h2>
              <p>
                Dán yêu cầu vào chatbot, rồi thay dòng trong ngoặc vuông bằng
                đoạn của bạn.
              </p>
            </div>
            <CopyPrompt
              key={`${platformId}-${skillId}-${scenarioId}`}
              text={starterPrompt(skill, scenarioId)}
            />
          </section>
        </div>
      </div>

      <div className={styles.support}>
        <section className={styles.fullGuide} aria-labelledby="starter-guide">
          <h2 id="starter-guide">Bộ hướng dẫn để đính kèm</h2>
          <p>
            Nếu chatbot đọc được tệp, hãy đính kèm bộ hướng dẫn. Ghi rõ phần bạn
            muốn dùng khi gửi văn bản.
          </p>
          <a
            href="/downloads/huong-dan-tieng-viet.md"
            download
            className="text-link action-link"
          >
            Tải bộ hướng dẫn đầy đủ
          </a>
        </section>

        <details className={styles.references}>
          <summary>Tài liệu chính thức của từng chatbot</summary>
          <p>
            Các bước được đối chiếu ngày {docsCheckedOn}. Tên mục và quyền sử
            dụng có thể khác tùy tài khoản hoặc phiên bản.
          </p>
          <ul>
            <li>
              <a
                className="text-link"
                href="https://learn.chatgpt.com/docs/plugins"
                target="_blank"
                rel="noopener noreferrer"
              >
                Cách dùng plugin trong ChatGPT
              </a>
            </li>
            <li>
              <a
                className="text-link"
                href="https://support.claude.com/en/articles/12512180-use-skills-in-claude"
                target="_blank"
                rel="noopener noreferrer"
              >
                Hướng dẫn skill của Claude
              </a>
            </li>
            <li>
              <a
                className="text-link"
                href="https://support.google.com/gemini/answer/17094296"
                target="_blank"
                rel="noopener noreferrer"
              >
                Hướng dẫn skill của Gemini
              </a>
            </li>
          </ul>
        </details>
      </div>
    </div>
  );
}
