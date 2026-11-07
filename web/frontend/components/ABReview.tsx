"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { FormEvent } from "react";
import Link from "next/link";
import { CapabilityProvider, useCapabilities } from "./CapabilityNav";
import { ApiError, fetchReviewAssignment, submitReviewVote } from "../lib/api";
import type {
  ReviewAssignmentResponse,
  ReviewChoice,
  ReviewReason,
  ReviewVoteRequest,
  ReviewVoteResponse,
} from "../lib/types";
import styles from "./ABReview.module.css";

const sessionKey = "vws:ab-review-session";
const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
let memorySession: string | undefined;

function createSession() {
  if (globalThis.crypto?.randomUUID) return globalThis.crypto.randomUUID();
  const bytes = new Uint8Array(16);
  if (globalThis.crypto?.getRandomValues) {
    globalThis.crypto.getRandomValues(bytes);
  } else {
    for (let index = 0; index < bytes.length; index += 1) {
      bytes[index] = Math.floor(Math.random() * 256);
    }
  }
  bytes[6] = (bytes[6] & 0x0f) | 0x40;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  const hex = Array.from(bytes, (byte) =>
    byte.toString(16).padStart(2, "0"),
  ).join("");
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}

function readSession() {
  try {
    const stored = localStorage.getItem(sessionKey);
    if (stored && uuid.test(stored)) memorySession = stored;
  } catch {
    // A blocked storage API leaves the current browser session in memory.
  }
  if (!memorySession) saveSession(createSession());
  return memorySession;
}

function saveSession(session: string) {
  memorySession = session;
  try {
    localStorage.setItem(sessionKey, session);
  } catch {
    // The next case can still use the in-memory session.
  }
}

const choices: { value: ReviewChoice; label: string }[] = [
  { value: "a", label: "Chọn A" },
  { value: "b", label: "Chọn B" },
  { value: "tie", label: "Hòa" },
  { value: "skip", label: "Bỏ qua" },
];
const reasonOptions: { value: ReviewReason; label: string }[] = [
  { value: "readability", label: "Dễ đọc" },
  { value: "register", label: "Hợp giọng" },
  { value: "meaning", label: "Giữ đúng ý" },
  { value: "restraint", label: "Sửa vừa đủ" },
];

const serviceMessages: Record<number, string> = {
  400: "Yêu cầu chấm A/B không hợp lệ. Bạn hãy tải lại trang.",
  422: "Yêu cầu chấm A/B không hợp lệ. Bạn hãy tải lại trang.",
  429: "Bạn đã gửi quá nhiều lượt. Chờ một phút rồi thử lại.",
  502: "Phần chấm A/B đang tạm nghỉ. Bạn hãy thử lại sau.",
  503: "Phần chấm A/B đang tạm nghỉ. Bạn hãy thử lại sau.",
  504: "Phần chấm A/B phản hồi chậm. Bạn hãy thử lại sau.",
};

function describeFailure(failure: unknown, fallback: string) {
  if (failure instanceof TypeError) {
    return {
      message: "Chưa kết nối được máy chủ. Bạn hãy thử lại sau.",
      retryable: true,
    };
  }
  if (failure instanceof ApiError) {
    return {
      message: serviceMessages[failure.status] ?? failure.message,
      retryable: failure.status === 429 || failure.status >= 500,
    };
  }
  if (failure instanceof Error) {
    return { message: failure.message, retryable: true };
  }
  return { message: fallback, retryable: true };
}

function LoadingReview({ children }: { children: React.ReactNode }) {
  return (
    <div className={styles.loading}>
      <p role="status">{children}</p>
      <div className={styles.skeleton} aria-hidden="true">
        <div />
        <div />
        <div />
      </div>
    </div>
  );
}

function ReviewBallot() {
  const session = useRef<string | undefined>(undefined);
  const generation = useRef(0);
  const submitting = useRef(false);
  const [data, setData] = useState<ReviewAssignmentResponse | null>(null);
  const [receipt, setReceipt] = useState<ReviewVoteResponse | null>(null);
  const [attempt, setAttempt] = useState<ReviewVoteRequest | null>(null);
  const [choice, setChoice] = useState<ReviewChoice | null>(null);
  const [reasons, setReasons] = useState<ReviewReason[]>([]);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [voteError, setVoteError] = useState<{
    message: string;
    retryable: boolean;
  } | null>(null);
  const caseHeading = useRef<HTMLHeadingElement>(null);
  const nextAction = useRef<HTMLButtonElement>(null);
  const completionHeading = useRef<HTMLHeadingElement>(null);
  const focusNext = useRef(false);
  const focusReceipt = useRef(false);

  const load = useCallback(async () => {
    const current = ++generation.current;
    session.current ??= readSession();
    try {
      const result = await fetchReviewAssignment(session.current);
      if (current !== generation.current) return;
      session.current = result.session_id;
      saveSession(result.session_id);
      setData(result);
    } catch (failure) {
      if (current === generation.current) {
        setLoadError(
          describeFailure(
            failure,
            "Chưa tải được cặp văn bản. Bạn hãy thử lại.",
          ).message,
        );
      }
    } finally {
      if (current === generation.current) setLoading(false);
    }
  }, []);

  function loadNext() {
    setLoading(true);
    setLoadError(null);
    setVoteError(null);
    setData(null);
    setReceipt(null);
    setAttempt(null);
    setChoice(null);
    setReasons([]);
    void load();
  }

  useEffect(() => {
    void load();
    return () => {
      generation.current += 1;
    };
  }, [load]);

  useEffect(() => {
    if (data?.assignment && focusNext.current) {
      caseHeading.current?.focus();
      focusNext.current = false;
    }
  }, [data]);

  useEffect(() => {
    if (!receipt || !focusReceipt.current) return;
    focusReceipt.current = false;
    if (receipt.completed >= receipt.total) completionHeading.current?.focus();
    else nextAction.current?.focus();
  }, [receipt]);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (
      !choice ||
      !data?.assignment ||
      !session.current ||
      submitting.current ||
      receipt
    )
      return;
    submitting.current = true;
    const current = generation.current;
    setSending(true);
    setVoteError(null);
    const currentPayload: ReviewVoteRequest = {
      session_id: session.current,
      assignment_id: data.assignment.id,
      choice,
      reasons: choice === "skip" ? [] : [...reasons],
    };
    const unchanged =
      attempt &&
      attempt.choice === currentPayload.choice &&
      attempt.assignment_id === currentPayload.assignment_id &&
      attempt.reasons.length === currentPayload.reasons.length &&
      attempt.reasons.every(
        (reason, index) => reason === currentPayload.reasons[index],
      );
    const payload = unchanged ? attempt : currentPayload;
    setAttempt(payload);
    try {
      const result = await submitReviewVote(payload);
      if (current === generation.current) {
        focusReceipt.current = true;
        setReceipt(result);
      }
    } catch (failure) {
      if (current === generation.current) {
        setVoteError(
          describeFailure(
            failure,
            "Chưa xác nhận được lựa chọn. Bạn hãy gửi lại.",
          ),
        );
      }
    } finally {
      if (current === generation.current) {
        submitting.current = false;
        setSending(false);
      }
    }
  }

  if (loading) return <LoadingReview>Đang tải cặp văn bản…</LoadingReview>;
  if (!data)
    return (
      <div className={styles.recovery}>
        {loadError && <p role="alert">{loadError}</p>}
        <button type="button" className="button-secondary" onClick={loadNext}>
          Thử tải lại
        </button>
        <Link className="text-link" href="/examples">
          Xem các ví dụ
        </Link>
      </div>
    );

  const counts = receipt ?? data;
  const skipped = counts.skipped ?? 0;
  const complete = !data.assignment || counts.completed >= counts.total;
  const currentAssignment = data.assignment;

  return (
    <>
      <div className={styles.study}>
        <div className={styles.studyIntro}>
          <p className={styles.studyTitle}>{data.study.title}</p>
          <details className={styles.disclosure}>
            <summary>Về đợt chấm</summary>
            <p>{data.study.disclosure}</p>
          </details>
        </div>
        <p className={styles.progress}>
          Đã xử lý {counts.completed}/{counts.total} cặp
        </p>
      </div>
      {complete ? (
        <section className={styles.complete} aria-labelledby="review-complete">
          <h2 id="review-complete" ref={completionHeading} tabIndex={-1}>
            Bạn đã chấm hết các cặp.
          </h2>
          <p role="status">
            Đã lưu {counts.completed - skipped} lượt so sánh và {skipped} lượt
            bỏ qua trong phiên này. Cảm ơn bạn đã góp ý.
          </p>
          <Link className="button-secondary" href="/examples">
            Xem các ví dụ
          </Link>
        </section>
      ) : (
        currentAssignment && (
          <div className={styles.workbench}>
            <section className={styles.source} aria-labelledby="review-topic">
              <h2 id="review-topic" ref={caseHeading} tabIndex={-1}>
                {currentAssignment.topic}
              </h2>
              <h3>Yêu cầu biên tập</h3>
              <p className={styles.verbatim}>{currentAssignment.instruction}</p>
              <h3>Đoạn gốc</h3>
              <p className={styles.verbatim}>{currentAssignment.input_text}</p>
              <p className={styles.pairNote}>
                Hai bản có thể chỉ khác vài chữ. Đọc kỹ câu mở đầu và câu kết.
              </p>{" "}
            </section>
            <div className={styles.outputs}>
              <section className={styles.output} aria-labelledby="review-a">
                <h3 id="review-a">Bản A</h3>
                <p className={styles.verbatim}>{currentAssignment.a}</p>
              </section>
              <section className={styles.output} aria-labelledby="review-b">
                <h3 id="review-b">Bản B</h3>
                <p className={styles.verbatim}>{currentAssignment.b}</p>
              </section>
            </div>
            <form
              className={styles.ballot}
              onSubmit={submit}
              aria-busy={sending}
            >
              <fieldset
                disabled={
                  sending || !!receipt || (!!voteError && !voteError.retryable)
                }
                className={styles.fields}
              >
                <legend>Bản nào đáp ứng yêu cầu tốt hơn?</legend>
                <div className={styles.choices}>
                  {choices.map((item) => (
                    <label className={styles.choice} key={item.value}>
                      <input
                        type="radio"
                        name="review-choice"
                        value={item.value}
                        checked={choice === item.value}
                        onChange={() => {
                          setChoice(item.value);
                          setAttempt(null);
                          if (item.value === "skip") setReasons([]);
                        }}
                      />
                      <span>{item.label}</span>
                    </label>
                  ))}
                </div>
                {choice && choice !== "skip" && (
                  <fieldset className={styles.reasons}>
                    <legend>
                      Lý do <span>(không bắt buộc)</span>
                    </legend>
                    <div className={styles.reasonOptions}>
                      {reasonOptions.map((item) => (
                        <label key={item.value}>
                          <input
                            type="checkbox"
                            checked={reasons.includes(item.value)}
                            onChange={(event) => {
                              setAttempt(null);
                              setReasons((selected) =>
                                event.target.checked
                                  ? [...selected, item.value]
                                  : selected.filter(
                                      (value) => value !== item.value,
                                    ),
                              );
                            }}
                          />
                          <span>{item.label}</span>
                        </label>
                      ))}
                    </div>
                  </fieldset>
                )}
              </fieldset>
              {receipt && (
                <p role="status" className={styles.receipt}>
                  {receipt.message}
                </p>
              )}
              {voteError && (
                <p className={styles.error} role="alert">
                  {voteError.message}
                  {voteError.retryable
                    ? " Lựa chọn được giữ; bạn có thể sửa rồi gửi lại."
                    : ""}
                </p>
              )}
              <div className={styles.submit}>
                {receipt ? (
                  <button
                    type="button"
                    ref={nextAction}
                    className="button-primary"
                    onClick={() => {
                      focusNext.current = true;
                      loadNext();
                    }}
                  >
                    Chấm cặp tiếp theo
                  </button>
                ) : voteError && !voteError.retryable ? (
                  <button
                    type="button"
                    className="button-secondary"
                    onClick={loadNext}
                  >
                    Tải lại cặp văn bản
                  </button>
                ) : (
                  <button
                    type="submit"
                    className="button-primary"
                    disabled={!choice || sending}
                  >
                    {sending ? "Đang gửi…" : "Gửi lựa chọn"}
                  </button>
                )}
                <p>
                  {voteError && !voteError.retryable
                    ? "Lượt này không thể gửi lại. Tải lại để nhận trạng thái mới."
                    : receipt
                      ? "Lượt đã lưu. Bạn có thể chấm tiếp hoặc dừng ở đây."
                      : "Hòa khi hai bản tương đương; Bỏ qua khi chưa đủ cơ sở để chọn."}
                </p>
              </div>
            </form>
          </div>
        )
      )}
      <p className={styles.privacy}>
        Lựa chọn được lưu để cải thiện bộ skill. Mã phiên ẩn danh giúp bạn tiếp
        tục trong trình duyệt này; số phiên không phải số người đã xác minh.
      </p>
    </>
  );
}

function ReviewContent() {
  const capabilities = useCapabilities();
  return (
    <div className={styles.page}>
      <header className={styles.heading}>
        <h1>Chấm A/B</h1>
        <p>
          Đọc đoạn gốc và yêu cầu biên tập, rồi chọn bản phù hợp hơn. Hai bản
          được giấu nhãn.
        </p>
      </header>
      {capabilities.status === "loading" ? (
        <LoadingReview>Đang kiểm tra khả năng chấm A/B…</LoadingReview>
      ) : capabilities.ab_review ? (
        <ReviewBallot />
      ) : (
        <div className={styles.recovery}>
          <p>
            {capabilities.status === "unavailable"
              ? "Chưa kết nối được với phần chấm A/B. Bạn có thể tải lại trang hoặc xem các ví dụ đã công khai."
              : "Phần chấm A/B hiện chưa mở. Bạn có thể đọc các ví dụ đã công khai."}
          </p>
          {capabilities.status === "unavailable" && (
            <a className="button-secondary" href="/review">
              Tải lại trang
            </a>
          )}
          <Link className="text-link" href="/examples">
            Xem các ví dụ
          </Link>
        </div>
      )}
    </div>
  );
}

export function ABReview() {
  return (
    <CapabilityProvider>
      <ReviewContent />
    </CapabilityProvider>
  );
}

function ReviewEntryContent() {
  const capabilities = useCapabilities();
  if (!capabilities.ab_review) return null;
  return (
    <section className={styles.entry} aria-labelledby="review-entry-title">
      <div>
        <h2 id="review-entry-title">Góp một lượt chấm A/B.</h2>
        <p>Đọc hai bản giấu nhãn và chọn bản phù hợp hơn.</p>
      </div>
      <Link className="button-secondary" href="/review">
        Chấm A/B
      </Link>
    </section>
  );
}

export function ABReviewEntry() {
  return (
    <CapabilityProvider>
      <ReviewEntryContent />
    </CapabilityProvider>
  );
}
