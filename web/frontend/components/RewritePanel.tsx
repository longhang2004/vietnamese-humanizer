import React, { useRef, useState } from "react";
import { rewriteText } from "../lib/api";
import { computeWordDiff } from "../lib/diff";
import { starterSkills } from "../lib/onboarding";
import type { RewriteResponse, RewriteStyle } from "../lib/types";
import { Icon } from "./Icon";
import styles from "./workspace.module.css";

const DEFAULT_STYLE: RewriteStyle = {
  profile: "preserve",
  channel: "auto",
  register: "preserve",
  audience: "",
  relationship: "",
  pronouns: "",
  voice_sample: "",
  edit_level: "light",
  reduce_hype: false,
};

const PROFILE_HINTS: Record<RewriteStyle["profile"], string> = {
  preserve: "Giữ loại bài và giọng hiện có; chỉ sửa những chỗ cần thiết.",
  plain: "Làm rõ mạch ý và quan hệ giữa các câu, giữ nét riêng của người viết.",
  business:
    "Làm rõ việc cần làm, trách nhiệm và thời hạn đã có trong nội dung.",
  technical: "Giữ chính xác điều kiện, thuật ngữ, code và thứ tự thao tác.",
  administrative:
    "Làm rõ nội dung, giữ đúng yêu cầu, thẩm quyền và mẫu văn bản đã có.",
  social: "Giữ giọng cá nhân, mạch chia sẻ và cách nói phù hợp với cộng đồng.",
  marketing: "Làm rõ sản phẩm, lợi ích có căn cứ và điều kiện ưu đãi.",
};

const CONTEXT_PRESETS: {
  id: string;
  label: string;
  profile: RewriteStyle["profile"];
  channel: RewriteStyle["channel"];
  register: RewriteStyle["register"];
  context: string;
}[] = [
  {
    id: "spoken_script",
    label: "Kịch bản nói / Vlog",
    profile: "plain",
    channel: "spoken_script",
    register: "conversational",
    context:
      "Kịch bản nói cho video hoặc vlog, ưu tiên câu nói miệng tự nhiên, nhịp ngắn.",
  },
  {
    id: "banter_social",
    label: "Bài đăng cợt nhả / Dí dỏm",
    profile: "social",
    channel: "chat",
    register: "conversational",
    context:
      "Bài đăng mạng xã hội giọng cợt nhả, dí dỏm; giữ điểm rơi câu đùa, không giải thích lại.",
  },
  {
    id: "satire",
    label: "Trào phúng / Châm biếm",
    profile: "social",
    channel: "document",
    register: "preserve",
    context:
      "Văn trào phúng, châm biếm; giữ nghịch ngữ, khen ngược và phép nhại văn phong.",
  },
];

const MODE_LABELS = {
  clean_rewrite: "Bản viết lại đề xuất",
  no_change: "Giữ nguyên văn bản",
  review_comment: "Nhận xét để bạn xem lại",
  needs_author_decision: "Cần tác giả quyết định",
};

interface RewritePanelProps {
  originalText: string;
  issueIds?: string[];
  selectedSkills?: string[];
  onApplyRewrite?: (nextText: string) => void;
}

export const RewritePanel: React.FC<RewritePanelProps> = ({
  originalText,
  issueIds,
  selectedSkills,
  onApplyRewrite,
}) => {
  const defaultSkill =
    selectedSkills?.length === 1 &&
    starterSkills.some((item) => item.id === selectedSkills[0])
      ? selectedSkills[0]
      : "humanizer-vi";
  const [skill, setSkill] = useState<string>(defaultSkill);
  const [style, setStyle] = useState<RewriteStyle>(DEFAULT_STYLE);
  const [context, setContext] = useState("");
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<RewriteResponse | null>(null);
  const [resultSource, setResultSource] = useState<string>("");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [copied, setCopied] = useState<boolean>(false);
  const [showDiff, setShowDiff] = useState<boolean>(false);
  const requestGeneration = useRef(0);
  const requestKey = JSON.stringify([
    originalText,
    skill,
    issueIds ?? null,
    context,
    style,
  ]);
  const visibleResult = resultSource === requestKey ? result : null;
  const visibleError = resultSource === requestKey ? errorMsg : null;
  const visibleLoading = resultSource === requestKey && loading;
  const outputMode = visibleResult?.output_mode ?? "clean_rewrite";
  const canCopy =
    Boolean(visibleResult?.rewrite) &&
    (outputMode === "clean_rewrite" || outputMode === "no_change");
  const canCompare =
    Boolean(visibleResult?.rewrite) &&
    outputMode === "clean_rewrite" &&
    visibleResult?.rewrite !== originalText;
  const matchedPresetId =
    CONTEXT_PRESETS.find(
      (preset) =>
        skill === "humanizer-vi" &&
        style.profile === preset.profile &&
        style.channel === preset.channel &&
        style.register === preset.register &&
        context === preset.context,
    )?.id ?? "";

  const invalidateResult = () => {
    requestGeneration.current += 1;
    setResult(null);
    setErrorMsg(null);
    setLoading(false);
    setCopied(false);
    setShowDiff(false);
  };

  const updateStyle = (patch: Partial<RewriteStyle>) => {
    invalidateResult();
    setStyle((previous) => ({ ...previous, ...patch }));
  };

  const applyPreset = (preset: (typeof CONTEXT_PRESETS)[number]) => {
    invalidateResult();
    setSkill("humanizer-vi");
    setStyle((previous) => ({
      ...previous,
      profile: preset.profile,
      channel: preset.channel,
      register: preset.register,
    }));
    setContext(preset.context);
  };

  const handleRewrite = async () => {
    if (!originalText.trim()) return;
    const generation = ++requestGeneration.current;
    setLoading(true);
    setErrorMsg(null);
    setCopied(false);
    setShowDiff(false);
    setResult(null);
    setResultSource(requestKey);
    try {
      const res = await rewriteText(originalText, skill, issueIds, {
        context,
        style,
      });
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
      setErrorMsg(
        "Chưa sao chép được. Bạn có thể chọn và sao chép văn bản trực tiếp.",
      );
    }
  };

  return (
    <section className={styles.rewrite} aria-labelledby="rewrite-title">
      <div className={styles.toolbar}>
        <div>
          <h2 id="rewrite-title">Gợi ý viết lại tự nhiên</h2>
          <p className={styles.rewriteIntro}>
            Gợi ý cách diễn đạt theo người đọc và ngữ cảnh. Bạn đọc lại trước
            khi dùng.
          </p>
        </div>
        <button
          type="button"
          onClick={handleRewrite}
          disabled={visibleLoading || !originalText.trim()}
          className="button-primary"
        >
          <Icon name="pen" />
          {visibleLoading ? "Đang viết lại…" : "Viết lại bằng Gemini"}
        </button>
      </div>

      <details className={styles.options}>
        <summary>Chọn giọng và ngữ cảnh (tùy chọn)</summary>
        <div className={`${styles.optionGrid} ${styles.rewriteOptions}`}>
          <div className={`${styles.formField} ${styles.fullWidth}`}>
            <span>Gợi ý nhanh theo ngữ cảnh</span>
            <div className={styles.presetRow}>
              {CONTEXT_PRESETS.map((preset) => (
                <button
                  key={preset.id}
                  type="button"
                  aria-pressed={matchedPresetId === preset.id}
                  onClick={() => applyPreset(preset)}
                  className={styles.filter}
                >
                  {preset.label}
                </button>
              ))}
            </div>
          </div>
          <label className={styles.formField}>
            <span>Kỹ năng viết lại</span>
            <select
              value={skill}
              onChange={(event) => {
                invalidateResult();
                setSkill(event.target.value);
              }}
              className="field"
            >
              {starterSkills.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.title}
                </option>
              ))}
            </select>
          </label>
          <div className={styles.formField}>
            <label htmlFor="writing-profile">Loại bài viết</label>
            <select
              id="writing-profile"
              value={style.profile}
              onChange={(event) =>
                updateStyle({
                  profile: event.target.value as RewriteStyle["profile"],
                })
              }
              aria-describedby="writing-profile-hint"
              className="field"
            >
              <option value="preserve">Giữ loại bài hiện có</option>
              <option value="plain">Văn viết phổ thông</option>
              <option value="business">Trao đổi công việc</option>
              <option value="technical">Tài liệu kỹ thuật</option>
              <option value="administrative">Văn bản hành chính</option>
              <option value="social">Bài đăng mạng xã hội</option>
              <option value="marketing">Marketing</option>
            </select>
            <p id="writing-profile-hint" className={styles.hint}>
              {PROFILE_HINTS[style.profile]}
            </p>
          </div>
          <label className={styles.formField}>
            <span>Kênh sử dụng</span>
            <select
              value={style.channel}
              onChange={(event) =>
                updateStyle({
                  channel: event.target.value as RewriteStyle["channel"],
                })
              }
              className="field"
            >
              <option value="auto">Theo văn bản gốc</option>
              <option value="document">Tài liệu / bài viết</option>
              <option value="email">Email</option>
              <option value="chat">Tin nhắn / trò chuyện</option>
              <option value="spoken_script">Kịch bản để đọc thành tiếng</option>
            </select>
          </label>
          <label className={styles.formField}>
            <span>Giọng mong muốn</span>
            <select
              value={style.register}
              onChange={(event) =>
                updateStyle({
                  register: event.target.value as RewriteStyle["register"],
                })
              }
              className="field"
            >
              <option value="preserve">Giữ giọng gốc</option>
              <option value="formal">Trang trọng</option>
              <option value="professional">Chuyên nghiệp, rõ ràng</option>
              <option value="friendly">Văn viết gần gũi</option>
              <option value="conversational">Giọng hội thoại</option>
            </select>
          </label>
          <label className={styles.formField}>
            <span>Mức can thiệp</span>
            <select
              value={style.edit_level}
              onChange={(event) =>
                updateStyle({
                  edit_level: event.target.value as RewriteStyle["edit_level"],
                })
              }
              className="field"
            >
              <option value="light">Nhẹ: sửa cục bộ</option>
              <option value="moderate">Vừa: gộp hoặc tách câu</option>
              <option value="deep">Sâu: có thể sắp xếp lại đoạn</option>
            </select>
          </label>
          <label className={styles.formField}>
            <span>Người đọc</span>
            <input
              value={style.audience}
              maxLength={300}
              placeholder="Ví dụ: người mới dùng sản phẩm"
              onChange={(event) =>
                updateStyle({ audience: event.target.value })
              }
              className="field"
            />
          </label>
          <label className={styles.formField}>
            <span>Quan hệ giao tiếp</span>
            <input
              value={style.relationship}
              maxLength={300}
              placeholder="Ví dụ: đồng nghiệp cùng nhóm"
              onChange={(event) =>
                updateStyle({ relationship: event.target.value })
              }
              className="field"
            />
          </label>
          <label className={styles.formField}>
            <span>Cách xưng hô</span>
            <input
              value={style.pronouns}
              maxLength={200}
              placeholder="Để trống để giữ cách xưng hô hiện có"
              onChange={(event) =>
                updateStyle({ pronouns: event.target.value })
              }
              className="field"
            />
          </label>
          <label className={`${styles.formField} ${styles.fullWidth}`}>
            <span>Ngữ cảnh bổ sung</span>
            <textarea
              value={context}
              maxLength={5000}
              rows={3}
              placeholder="Mục đích, thông tin liên quan hoặc phần hội thoại trước đó"
              onChange={(event) => {
                invalidateResult();
                setContext(event.target.value);
              }}
              className="field"
            />
          </label>
          <label className={`${styles.formField} ${styles.fullWidth}`}>
            <span>Đoạn mẫu giọng viết (tùy chọn)</span>
            <textarea
              value={style.voice_sample ?? ""}
              maxLength={1500}
              rows={3}
              placeholder="Dán 1–2 đoạn bạn từng viết để bám theo nhịp và cách xưng hô quen thuộc; công cụ không lấy dữ kiện từ đoạn mẫu."
              onChange={(event) =>
                updateStyle({ voice_sample: event.target.value })
              }
              className="field"
            />
          </label>
          <label className={`${styles.consent} ${styles.fullWidth}`}>
            <input
              type="checkbox"
              checked={style.reduce_hype}
              onChange={(event) =>
                updateStyle({ reduce_hype: event.target.checked })
              }
            />
            <span>
              Cho phép giảm lời khen quá mức và lời đồng cảm theo khuôn. Cảm xúc
              có thể được diễn đạt nhẹ hơn; dữ kiện và cam kết vẫn phải giữ
              nguyên.
            </span>
          </label>
        </div>
      </details>

      <p role="status" aria-atomic="true" className="sr-only">
        {visibleLoading
          ? "Đang tạo gợi ý viết lại."
          : copied
            ? "Đã sao chép kết quả."
            : ""}
      </p>
      {visibleError && (
        <div role="alert" className={styles.feedback}>
          <h3 className={styles.danger}>Chưa thực hiện được</h3>
          <p>{visibleError}</p>
        </div>
      )}
      {visibleLoading && (
        <div
          aria-busy="true"
          aria-label="Đang tạo gợi ý viết lại"
          className={styles.skeleton}
        >
          <div aria-hidden="true" className={styles.skeletonItem}>
            <div className={styles.skeletonLine} />
            <div className={styles.skeletonLine} />
            <div className={styles.skeletonLine} />
          </div>
        </div>
      )}
      {visibleResult && (
        <div className={styles.rewriteOutput}>
          <div className={styles.rewriteMeta}>
            <div>
              <span className={styles.reviewStatus}>
                {visibleResult.review_status === "unreviewed"
                  ? "Chưa được duyệt"
                  : visibleResult.review_status}
              </span>
              <p>{visibleResult.disclaimer}</p>
            </div>
            {(canCompare || canCopy) && (
              <div className={styles.rewriteActions}>
                {canCompare && (
                  <button
                    type="button"
                    aria-pressed={showDiff}
                    onClick={() => setShowDiff((current) => !current)}
                    className={styles.filter}
                  >
                    So sánh thay đổi
                  </button>
                )}
                {canCopy && onApplyRewrite && (
                  <button
                    type="button"
                    onClick={() => onApplyRewrite(visibleResult.rewrite)}
                    className="button-secondary"
                  >
                    Đưa vào ô soát tiếp
                  </button>
                )}
                {canCopy && (
                  <button
                    type="button"
                    onClick={handleCopy}
                    className="button-secondary"
                  >
                    <Icon name={copied ? "check" : "copy"} />
                    {copied ? "Đã sao chép" : "Sao chép kết quả"}
                  </button>
                )}
              </div>
            )}
          </div>
          <div className={styles.textPair}>
            <div className={styles.outputText}>
              <h3>Văn bản gốc:</h3>
              <p>{originalText}</p>
            </div>
            <div className={styles.outputText}>
              <h3>{MODE_LABELS[outputMode]}:</h3>
              {canCopy &&
                (showDiff && outputMode === "clean_rewrite" ? (
                  <p>
                    {computeWordDiff(originalText, visibleResult.rewrite).map(
                      (segment, index) =>
                        segment.kind === "removed" ? (
                          <del key={index} className={styles.diffRemoved}>
                            {segment.text}
                          </del>
                        ) : segment.kind === "added" ? (
                          <ins key={index} className={styles.diffAdded}>
                            {segment.text}
                          </ins>
                        ) : (
                          <React.Fragment key={index}>
                            {segment.text}
                          </React.Fragment>
                        ),
                    )}
                  </p>
                ) : (
                  <p>{visibleResult.rewrite}</p>
                ))}
              {Boolean(visibleResult.comments?.length) && (
                <ul>
                  {visibleResult.comments?.map((comment, index) => (
                    <li key={index}>{comment}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      )}
    </section>
  );
};
