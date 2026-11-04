import React, { useRef, useState } from "react";
import { rewriteText } from "../lib/api";
import { RewriteResponse, RewriteStyle } from "../lib/types";

const DEFAULT_STYLE: RewriteStyle = {
  profile: "preserve", channel: "auto", register: "preserve", audience: "", relationship: "", pronouns: "",
  edit_level: "light", reduce_hype: false,
};

const PROFILE_HINTS: Record<RewriteStyle["profile"], string> = {
  preserve: "Giữ loại bài và giọng hiện có; chỉ sửa những chỗ cần thiết.",
  plain: "Làm rõ mạch ý và quan hệ giữa các câu, giữ nét riêng của người viết.",
  business: "Làm rõ việc cần làm, trách nhiệm và thời hạn đã có trong nội dung.",
  technical: "Giữ chính xác điều kiện, thuật ngữ, code và thứ tự thao tác.",
  administrative: "Làm rõ nội dung, giữ đúng yêu cầu, thẩm quyền và mẫu văn bản đã có.",
  social: "Giữ giọng cá nhân, mạch chia sẻ và cách nói phù hợp với cộng đồng.",
  marketing: "Làm rõ sản phẩm, lợi ích có căn cứ và điều kiện ưu đãi.",
};

const MODE_LABELS = {
  clean_rewrite: "Bản viết lại đề xuất",
  no_change: "Giữ nguyên văn bản",
  review_comment: "Nhận xét để bạn xem lại",
  needs_author_decision: "Cần tác giả quyết định",
};

interface RewritePanelProps {
  originalText: string;
  issueIds?: string[];
}

export const RewritePanel: React.FC<RewritePanelProps> = ({ originalText, issueIds }) => {
  const [style, setStyle] = useState<RewriteStyle>(DEFAULT_STYLE);
  const [context, setContext] = useState("");
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<RewriteResponse | null>(null);
  const [resultSource, setResultSource] = useState<string>("");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [copied, setCopied] = useState<boolean>(false);
  const requestGeneration = useRef(0);
  const requestKey = JSON.stringify([originalText, issueIds ?? null, context, style]);
  const visibleResult = resultSource === requestKey ? result : null;
  const visibleError = resultSource === requestKey ? errorMsg : null;
  const visibleLoading = resultSource === requestKey && loading;
  const outputMode = visibleResult?.output_mode ?? "clean_rewrite";
  const canCopy = Boolean(visibleResult?.rewrite) &&
    (outputMode === "clean_rewrite" || outputMode === "no_change");

  const invalidateResult = () => {
    requestGeneration.current += 1;
    setResult(null);
    setErrorMsg(null);
    setLoading(false);
    setCopied(false);
  };

  const updateStyle = (patch: Partial<RewriteStyle>) => {
    invalidateResult();
    setStyle((previous) => ({ ...previous, ...patch }));
  };

  const handleRewrite = async () => {
    if (!originalText.trim()) return;
    const generation = ++requestGeneration.current;
    setLoading(true);
    setErrorMsg(null);
    setCopied(false);
    setResult(null);
    setResultSource(requestKey);
    try {
      const res = await rewriteText(originalText, "humanizer-vi", issueIds, { context, style });
      if (generation !== requestGeneration.current) return;
      setResult(res);
      setResultSource(requestKey);
    } catch (err: unknown) {
      if (generation !== requestGeneration.current) return;
      if (err instanceof Error) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg("Chưa tạo được gợi ý viết lại. Bạn hãy thử lại.");
      }
    } finally {
      if (generation === requestGeneration.current) {
        setLoading(false);
      }
    }
  };

  const handleCopy = async () => {
    if (!canCopy || !visibleResult) return;
    try {
      await navigator.clipboard.writeText(visibleResult.rewrite);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      setErrorMsg("Chưa sao chép được. Bạn có thể chọn và sao chép văn bản trực tiếp.");
    }
  };

  return (
    <div className="bg-[var(--surface)] rounded-2xl  border border-[var(--border)] p-5 sm:p-6 mb-8 transition-all">
      <div className="flex flex-wrap justify-between items-center gap-4 mb-4 pb-4 border-b border-[var(--border)]">
        <div>
          <h2 className="text-base sm:text-lg font-bold text-[var(--foreground)] tracking-tight flex items-center gap-2">
            <svg className="w-5 h-5 text-[var(--accent)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
            </svg>
            <span>Gợi ý viết lại tự nhiên</span>
          </h2>
          <p className="text-xs text-[var(--muted)] mt-1 leading-normal">
            Gợi ý cách diễn đạt theo người đọc và ngữ cảnh. Bạn đọc lại trước khi dùng.
          </p>
        </div>

        <button
          type="button"
          onClick={handleRewrite}
          disabled={visibleLoading || !originalText.trim()}
          className="px-5 py-2.5 bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-[var(--accent-ink)] font-bold text-xs sm:text-sm rounded-xl   disabled:opacity-50 disabled:cursor-not-allowed  active:scale-[0.98] transition-all flex items-center space-x-2"
        >
          {visibleLoading ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-[var(--accent-ink)]" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              <span>Đang viết lại...</span>
            </>
          ) : (
            <>
              <svg className="w-4 h-4 text-[var(--accent)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
              </svg>
              <span>Viết lại bằng Gemini</span>
            </>
          )}
        </button>
      </div>

      <details className="mb-4 rounded-xl border border-[var(--border)] bg-[var(--surface-raised)] p-4">
        <summary className="cursor-pointer text-sm font-semibold text-[var(--foreground)]">
          Chọn giọng và ngữ cảnh (tùy chọn)
        </summary>
        <p className="mt-2 text-xs text-[var(--muted)]">Mặc định giữ giọng gốc và sửa nhẹ. Nếu muốn đổi cách xưng hô, hãy ghi rõ ở ô bên dưới, kể cả khi chọn chat.</p>
        <div className="mt-4 grid gap-4 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <label className="text-sm text-[var(--muted)]">Loại bài viết
              <select value={style.profile} aria-describedby="writing-profile-hint" onChange={(event) => updateStyle({ profile: event.target.value as RewriteStyle["profile"] })} className="mt-1 block w-full rounded-lg border border-[var(--border)] bg-[var(--surface)] p-2">
                <option value="preserve">Theo văn bản gốc</option>
                <option value="plain">Văn viết rõ ràng</option>
                <option value="business">Trao đổi công việc</option>
                <option value="technical">Tài liệu kỹ thuật</option>
                <option value="administrative">Văn bản hành chính</option>
                <option value="social">Bài đăng mạng xã hội</option>
                <option value="marketing">Marketing</option>
              </select>
            </label>
            <p id="writing-profile-hint" className="mt-1 text-xs text-[var(--muted)]">{PROFILE_HINTS[style.profile]} Bạn vẫn có thể chọn kênh, giọng và mức sửa bên dưới.</p>
          </div>
          <label className="text-sm text-[var(--muted)]">Kênh sử dụng
            <select value={style.channel} onChange={(event) => updateStyle({ channel: event.target.value as RewriteStyle["channel"] })} className="mt-1 block w-full rounded-lg border border-[var(--border)] bg-[var(--surface)] p-2">
              <option value="auto">Theo văn bản gốc</option>
              <option value="document">Tài liệu / bài viết</option>
              <option value="email">Email</option>
              <option value="chat">Tin nhắn / trò chuyện</option>
              <option value="spoken_script">Kịch bản để đọc thành tiếng</option>
            </select>
          </label>
          <label className="text-sm text-[var(--muted)]">Giọng mong muốn
            <select value={style.register} onChange={(event) => updateStyle({ register: event.target.value as RewriteStyle["register"] })} className="mt-1 block w-full rounded-lg border border-[var(--border)] bg-[var(--surface)] p-2">
              <option value="preserve">Giữ giọng gốc</option>
              <option value="formal">Trang trọng</option>
              <option value="professional">Chuyên nghiệp, rõ ràng</option>
              <option value="friendly">Văn viết gần gũi</option>
              <option value="conversational">Giọng hội thoại</option>
            </select>
          </label>
          <label className="text-sm text-[var(--muted)]">Người đọc
            <input value={style.audience} maxLength={300} placeholder="Ví dụ: người mới dùng sản phẩm" onChange={(event) => updateStyle({ audience: event.target.value })} className="mt-1 block w-full rounded-lg border border-[var(--border)] bg-[var(--surface)] p-2" />
          </label>
          <label className="text-sm text-[var(--muted)]">Quan hệ giao tiếp
            <input value={style.relationship} maxLength={300} placeholder="Ví dụ: đồng nghiệp cùng nhóm" onChange={(event) => updateStyle({ relationship: event.target.value })} className="mt-1 block w-full rounded-lg border border-[var(--border)] bg-[var(--surface)] p-2" />
          </label>
          <label className="text-sm text-[var(--muted)]">Cách xưng hô
            <input value={style.pronouns} maxLength={200} placeholder="Để trống để giữ cách xưng hô hiện có" onChange={(event) => updateStyle({ pronouns: event.target.value })} className="mt-1 block w-full rounded-lg border border-[var(--border)] bg-[var(--surface)] p-2" />
          </label>
          <label className="text-sm text-[var(--muted)]">Mức can thiệp
            <select value={style.edit_level} onChange={(event) => updateStyle({ edit_level: event.target.value as RewriteStyle["edit_level"] })} className="mt-1 block w-full rounded-lg border border-[var(--border)] bg-[var(--surface)] p-2">
              <option value="light">Nhẹ: sửa cục bộ</option>
              <option value="moderate">Vừa: gộp hoặc tách câu</option>
              <option value="deep">Sâu: có thể sắp xếp lại đoạn</option>
            </select>
          </label>
          <label className="text-sm text-[var(--muted)] sm:col-span-2">Ngữ cảnh bổ sung
            <textarea value={context} maxLength={5000} rows={3} placeholder="Mục đích, thông tin liên quan hoặc phần hội thoại trước đó" onChange={(event) => { invalidateResult(); setContext(event.target.value); }} className="mt-1 block w-full rounded-lg border border-[var(--border)] bg-[var(--surface)] p-2" />
          </label>
          <label className="flex items-start gap-2 text-sm text-[var(--muted)] sm:col-span-2">
            <input type="checkbox" checked={style.reduce_hype} onChange={(event) => updateStyle({ reduce_hype: event.target.checked })} className="mt-1" />
            <span>Cho phép giảm lời khen quá mức và lời đồng cảm theo khuôn. Cảm xúc có thể được diễn đạt nhẹ hơn; dữ kiện và cam kết vẫn phải giữ nguyên.</span>
          </label>
        </div>
      </details>

      {visibleError && (
        <div className="p-3.5 bg-[var(--surface-raised)] border border-[var(--border)] text-[var(--warning)] rounded-xl text-xs mb-4">
          <span className="font-bold">Chưa thực hiện được:</span> {visibleError}
        </div>
      )}

      {visibleResult && (
        <div className="mt-4 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 bg-[var(--surface-raised)] p-3 rounded-xl border border-[var(--border)]">
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-1 bg-[var(--surface-raised)] text-[var(--warning)] text-[11px] font-mono font-bold rounded-full border border-[var(--border)] uppercase tracking-wider">
                {visibleResult.review_status === "unreviewed" ? "Chưa được duyệt" : visibleResult.review_status}
              </span>
              <span className="text-xs text-[var(--muted)] italic">{visibleResult.disclaimer}</span>
            </div>

            {canCopy && <button
              type="button"
              onClick={handleCopy}
              className="px-3 py-1 bg-[var(--surface)] hover:bg-[var(--surface-raised)] text-[var(--muted)] text-xs font-semibold rounded-lg border border-[var(--border)]  flex items-center space-x-1.5 transition-all"
            >
              {copied ? (
                <>
                  <svg className="w-3.5 h-3.5 text-[var(--accent)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                  </svg>
                  <span className="text-[var(--accent)] font-bold">Đã sao chép</span>
                </>
              ) : (
                <>
                  <svg className="w-3.5 h-3.5 text-[var(--muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.757c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 011.927-.184" />
                  </svg>
                  <span>Sao chép kết quả</span>
                </>
              )}
            </button>}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div className="p-4 bg-[var(--surface-raised)] rounded-xl border border-[var(--border)] text-xs sm:text-sm">
              <span className="block font-bold text-[var(--muted)] text-xs uppercase tracking-wider font-mono mb-2">
                Văn bản gốc:
              </span>
              <p className="whitespace-pre-wrap text-[var(--foreground)] leading-relaxed font-sans">{originalText}</p>
            </div>

            <div className="p-4 bg-[var(--surface-raised)] rounded-xl border border-[var(--border)] text-xs sm:text-sm">
              <span className="block font-bold text-[var(--accent)] text-xs uppercase tracking-wider font-mono mb-2 flex items-center justify-between">
                <span>{MODE_LABELS[outputMode]}:</span>
                <span className="text-[10px] text-[var(--accent)] bg-[var(--surface-raised)] px-2 py-0.5 rounded">Cần tác giả duyệt</span>
              </span>
              {canCopy && <p className="whitespace-pre-wrap text-[var(--accent)] font-medium leading-relaxed font-sans">
                {visibleResult.rewrite}
              </p>}
              {Boolean(visibleResult.comments?.length) && <ul className="list-disc pl-5 space-y-2 text-[var(--foreground)] leading-relaxed">
                {visibleResult.comments?.map((comment, index) => <li key={index}>{comment}</li>)}
              </ul>}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

