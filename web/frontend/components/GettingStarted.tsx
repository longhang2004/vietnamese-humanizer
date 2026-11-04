"use client";

import Link from "next/link";
import { useState } from "react";
import {
  chatgptInstallUrl, docsCheckedOn, Platform, skillDownload, starterPrompt, starterSkills,
} from "../lib/onboarding";

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
      setMessage("Chưa sao chép được. Bạn có thể chọn toàn bộ nội dung trong ô bên dưới và sao chép trực tiếp.");
    }
  }

  return (
    <div className="space-y-3">
      <button type="button" onClick={copy} className="rounded-xl bg-sky-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-sky-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-600">
        Sao chép yêu cầu
      </button>
      <p role="status" className="text-sm text-sky-800">{message}</p>
      <label className="block text-sm font-medium text-slate-700" htmlFor="starter-prompt">
        Yêu cầu mẫu để sao chép
      </label>
      <textarea id="starter-prompt" readOnly value={text} rows={8} className="w-full rounded-xl border border-slate-300 bg-slate-50 p-4 text-sm leading-relaxed text-slate-700 focus:border-sky-500 focus:outline-none focus:ring-2 focus:ring-sky-100" />
    </div>
  );
}

export function GettingStarted() {
  const [platformId, setPlatformId] = useState<Platform>("chatgpt");
  const [skillId, setSkillId] = useState(starterSkills[0].id);
  const platform = PLATFORMS.find((item) => item.id === platformId)!;
  const skill = starterSkills.find((item) => item.id === skillId)!;
  const nativePlatform = platformId === "claude" || platformId === "gemini" ? platformId : null;
  const download = nativePlatform ? skillDownload(nativePlatform, skill) : null;

  return (
    <div className="mx-auto max-w-4xl space-y-8">
      <section className="rounded-3xl border border-sky-100 bg-gradient-to-br from-sky-50 via-white to-emerald-50 p-6 sm:p-10">
        <p className="text-sm font-semibold text-sky-700">Vietnamese Writing Skills</p>
        <h1 className="mt-3 max-w-2xl text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
          Viết tiếng Việt tự nhiên hơn với chatbot bạn đang dùng
        </h1>
        <p className="mt-4 max-w-2xl text-base leading-relaxed text-slate-600">
          Chọn chatbot và việc bạn muốn làm.
        </p>
        <Link href="/" className="mt-5 inline-block text-sm font-semibold text-sky-700 underline decoration-sky-200 underline-offset-4 hover:text-sky-900">
          Soát văn phong ngay trên web →
        </Link>
      </section>

      <section className="space-y-7 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-8">
        <fieldset>
          <legend className="mb-3 text-lg font-semibold text-slate-900">1. Bạn đang dùng công cụ nào?</legend>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
            {PLATFORMS.map((item) => (
              <button key={item.id} type="button" aria-pressed={platformId === item.id} onClick={() => setPlatformId(item.id)} className={`rounded-xl border px-3 py-3 text-sm font-semibold transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-600 ${platformId === item.id ? "border-sky-600 bg-sky-50 text-sky-800" : "border-slate-200 text-slate-600 hover:border-sky-300"}`}>
                {item.label}
              </button>
            ))}
          </div>
        </fieldset>

        <div>
          <label htmlFor="starter-task" className="mb-3 block text-lg font-semibold text-slate-900">2. Chọn việc muốn làm</label>
          <select id="starter-task" value={skillId} onChange={(event) => setSkillId(event.target.value)} className="w-full rounded-xl border border-slate-300 bg-white p-3 text-base text-slate-800 focus:border-sky-500 focus:outline-none focus:ring-2 focus:ring-sky-100">
            {starterSkills.map((item) => <option key={item.id} value={item.id}>{item.title}</option>)}
          </select>
          <p className="mt-2 text-sm leading-relaxed text-slate-600">{skill.summary}</p>
        </div>

        <div className="border-t border-slate-100 pt-6">
          <h2 className="text-lg font-semibold text-slate-900">3. Bắt đầu với {platform.label}</h2>
          {download && <div className="mt-4 space-y-4">
            <a href={download.href} download className="inline-flex max-w-full flex-wrap items-center gap-2 rounded-xl bg-emerald-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-emerald-700">
              Tải skill “{skill.title}” <span className="text-xs font-normal text-emerald-100">ZIP · {download.size}</span>
            </a>
            <div aria-hidden="true" className="grid grid-cols-3 gap-2 rounded-xl bg-slate-50 p-3 text-center text-xs font-medium text-slate-600">
              {[
                { label: "Tải về", path: "M12 3v12m-4-4 4 4 4-4M5 16v4h14v-4" },
                { label: "Thêm skill", path: "M3 7h7l2 2h9v11H3ZM12 11v6m-3-3h6" },
                { label: "Thử với văn bản của bạn", path: "M5 4h14v13H9l-4 4Zm4 5h6m-6 4h4" },
              ].map((step) => <div key={step.label}>
                <svg className="mx-auto mb-2 h-7 w-7 text-sky-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d={step.path} /></svg>
                {step.label}
              </div>)}
            </div>
            <ol className="list-decimal space-y-2 pl-5 text-sm leading-relaxed text-slate-700">
              <li>Tải tệp ZIP ở trên về máy.</li>
              {platformId === "claude" ? <>
                <li>Mở Claude → Customize → Skills → thêm skill → Upload a skill, rồi chọn tệp vừa tải.</li>
                <li>Bật skill. Nếu Claude yêu cầu, bật Code execution and file creation trong Settings → Capabilities.</li>
              </> : <>
                <li>Trên web Gemini, mở Customize → Skills → Create → Upload, rồi chọn tệp vừa tải.</li>
                <li>Xem lại nội dung rồi chọn Create.</li>
              </>}
              <li>Mở cuộc trò chuyện mới, dán yêu cầu mẫu bên dưới và thêm văn bản của bạn.</li>
            </ol>
            <p className="text-sm text-slate-600">
              Nếu chưa thấy mục Skills, bạn vẫn có thể dùng yêu cầu mẫu bên dưới.
            </p>
          </div>}
          {platformId === "chatgpt" && <div className="mt-3 space-y-3 text-sm leading-relaxed text-slate-700">
            {chatgptInstallUrl ? <a href={chatgptInstallUrl} target="_blank" rel="noopener noreferrer" className="inline-block rounded-xl bg-emerald-600 px-5 py-3 font-semibold text-white hover:bg-emerald-700">Cài plugin trong ChatGPT</a> : <p>Dùng ngay bằng cách sao chép yêu cầu mẫu, mở ChatGPT và dán vào cuộc trò chuyện mới.</p>}
          </div>}
          {platformId === "other" && <p className="mt-3 text-sm leading-relaxed text-slate-700">
            Sao chép yêu cầu mẫu và dán vào chatbot của bạn. Nếu chatbot cho đính kèm tài liệu, bạn có thể thêm bộ hướng dẫn đầy đủ bên dưới.
          </p>}
          {platform.url && <a href={platform.url} target="_blank" rel="noopener noreferrer" className="mt-4 inline-block text-sm font-semibold text-sky-700 underline decoration-sky-200 underline-offset-4 hover:text-sky-900">
            Mở {platform.label} ↗
          </a>}
        </div>

        <div className="border-t border-slate-100 pt-6">
          <h2 className="mb-3 text-lg font-semibold text-slate-900">Thử với văn bản của bạn</h2>
          <p className="mb-4 text-sm leading-relaxed text-slate-600">Thay phần [Dán văn bản của bạn vào đây] bằng đoạn cần sửa.</p>
          <CopyPrompt key={`${platformId}-${skillId}`} text={starterPrompt(skill)} />
        </div>
      </section>

      <section>
        <div className="rounded-2xl border border-slate-200 bg-white p-5">
          <h2 className="font-semibold text-slate-900">Dùng bộ hướng dẫn đầy đủ</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-600">Nếu chatbot hỗ trợ đọc tệp, bạn có thể đính kèm bộ hướng dẫn đầy đủ. Trong yêu cầu, hãy nói rõ phần bạn muốn chatbot áp dụng.</p>
          <a href="/downloads/huong-dan-tieng-viet.md" download className="mt-3 inline-block text-sm font-semibold text-sky-700 underline underline-offset-4">Tải bộ hướng dẫn đầy đủ</a>
        </div>
      </section>

      <details className="rounded-xl border border-slate-200 p-4 text-sm text-slate-600">
        <summary className="cursor-pointer font-medium">Hướng dẫn cài đặt chính thức</summary>
        <p className="mt-3">Đã đối chiếu các bước với tài liệu chính thức ngày {docsCheckedOn}. Giao diện có thể khác tùy tài khoản và phiên bản ứng dụng.</p>
        {!chatgptInstallUrl && <p className="mt-3">Gói plugin ChatGPT chưa được phát hành công khai.</p>}
        <ul className="mt-3 list-disc space-y-2 pl-5">
          <li><a className="underline underline-offset-4" href="https://learn.chatgpt.com/docs/plugins" target="_blank" rel="noopener noreferrer">Plugin trong ChatGPT</a></li>
          <li><a className="underline underline-offset-4" href="https://support.claude.com/en/articles/12512180-use-skills-in-claude" target="_blank" rel="noopener noreferrer">Cài và dùng skill trong Claude</a></li>
          <li><a className="underline underline-offset-4" href="https://support.google.com/gemini/answer/17094296" target="_blank" rel="noopener noreferrer">Cài và dùng skill trong Gemini</a></li>
        </ul>
      </details>
    </div>
  );
}
