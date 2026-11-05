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
      setMessage("Đã sao chép.");
    } catch {
      setMessage(
        "Chưa sao chép được. Bạn có thể chọn toàn bộ nội dung trong ô yêu cầu mẫu và sao chép trực tiếp.",
      );
    }
  }

  return (
    <div className={styles.copyPrompt}>
      <div className={styles.promptControls}>
        <label className={styles.promptLabel} htmlFor="starter-prompt">
          Yêu cầu mẫu để sao chép
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
  const platform = PLATFORMS.find((item) => item.id === platformId)!;
  const skill = starterSkills.find((item) => item.id === skillId)!;
  const nativePlatform =
    platformId === "claude" || platformId === "gemini" ? platformId : null;
  const download = nativePlatform ? skillDownload(nativePlatform, skill) : null;

  return (
    <div className={styles.page}>
      <header className={`page-heading ${styles.header}`}>
        <div>
          <h1>Viết tiếng Việt tự nhiên hơn với chatbot bạn đang dùng</h1>
          <p>Chọn chatbot và việc bạn muốn làm.</p>
        </div>
        <Link href="/check" className="text-link action-link">
          Soát văn phong ngay trên web
          <Icon name="arrow" width="16" height="16" />
        </Link>
      </header>

      <div className={styles.workspace}>
        <aside
          className={styles.choices}
          aria-label="Chọn chatbot và việc cần làm"
        >
          <fieldset>
            <legend>Bạn đang dùng công cụ nào?</legend>
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
            <label htmlFor="starter-task">Chọn việc muốn làm</label>
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
          </div>
        </aside>

        <div className={styles.content}>
          <section className={styles.setup} aria-labelledby="starter-setup">
            <h2 id="starter-setup">Bắt đầu với {platform.label}</h2>
            {download && (
              <div className={styles.nativeSetup}>
                <a href={download.href} download className="button-primary">
                  <span>Tải skill “{skill.title}”</span>
                  <span className={styles.downloadSize}>
                    ZIP · {download.size}
                  </span>
                </a>
                <ol>
                  <li>Tải tệp ZIP ở trên về máy.</li>
                  {platformId === "claude" ? (
                    <>
                      <li>
                        Mở Claude → Customize → Skills → thêm skill → Upload a
                        skill, rồi chọn tệp vừa tải.
                      </li>
                      <li>
                        Bật skill. Nếu Claude yêu cầu, bật Code execution and
                        file creation trong Settings → Capabilities.
                      </li>
                    </>
                  ) : (
                    <>
                      <li>
                        Trên web Gemini, mở Customize → Skills → Create →
                        Upload, rồi chọn tệp vừa tải.
                      </li>
                      <li>Xem lại nội dung rồi chọn Create.</li>
                    </>
                  )}
                  <li>
                    Mở cuộc trò chuyện mới, dán yêu cầu mẫu bên dưới và thêm văn
                    bản của bạn.
                  </li>
                </ol>
                <p>
                  Nếu chưa thấy mục Skills, bạn vẫn có thể dùng yêu cầu mẫu bên
                  dưới.
                </p>
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
                    Dùng ngay bằng cách sao chép yêu cầu mẫu, mở ChatGPT và dán
                    vào cuộc trò chuyện mới.
                  </p>
                )}
              </div>
            )}
            {platformId === "other" && (
              <p className={styles.platformSetup}>
                Sao chép yêu cầu mẫu và dán vào chatbot của bạn. Nếu chatbot cho
                đính kèm tài liệu, bạn có thể thêm bộ hướng dẫn đầy đủ bên dưới.
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
              <h2 id="starter-try">Thử với văn bản của bạn</h2>
              <p>Thay phần [Dán văn bản của bạn vào đây] bằng đoạn cần sửa.</p>
            </div>
            <CopyPrompt
              key={`${platformId}-${skillId}`}
              text={starterPrompt(skill)}
            />
          </section>
        </div>
      </div>

      <div className={styles.support}>
        <section className={styles.fullGuide} aria-labelledby="starter-guide">
          <h2 id="starter-guide">Dùng bộ hướng dẫn đầy đủ</h2>
          <p>
            Nếu chatbot hỗ trợ đọc tệp, bạn có thể đính kèm bộ hướng dẫn đầy đủ.
            Trong yêu cầu, hãy nói rõ phần bạn muốn chatbot áp dụng.
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
          <summary>Hướng dẫn cài đặt chính thức</summary>
          <p>
            Đã đối chiếu các bước với tài liệu chính thức ngày {docsCheckedOn}.
            Giao diện có thể khác tùy tài khoản và phiên bản ứng dụng.
          </p>
          {!chatgptInstallUrl && (
            <p>Gói plugin ChatGPT chưa được phát hành công khai.</p>
          )}
          <ul>
            <li>
              <a
                className="text-link"
                href="https://learn.chatgpt.com/docs/plugins"
                target="_blank"
                rel="noopener noreferrer"
              >
                Plugin trong ChatGPT
              </a>
            </li>
            <li>
              <a
                className="text-link"
                href="https://support.claude.com/en/articles/12512180-use-skills-in-claude"
                target="_blank"
                rel="noopener noreferrer"
              >
                Cài và dùng skill trong Claude
              </a>
            </li>
            <li>
              <a
                className="text-link"
                href="https://support.google.com/gemini/answer/17094296"
                target="_blank"
                rel="noopener noreferrer"
              >
                Cài và dùng skill trong Gemini
              </a>
            </li>
          </ul>
        </details>
      </div>
    </div>
  );
}
