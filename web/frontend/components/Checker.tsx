"use client";

import React, { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useCapabilities } from "./CapabilityNav";
import { Editor } from "./Editor";
import { IssueList } from "./IssueList";
import { RewritePanel } from "./RewritePanel";
import { fetchPatterns, fetchSkills, lintText } from "../lib/api";
import type { LintResponse, PatternItem, SkillItem } from "../lib/types";
import styles from "./workspace.module.css";

export function Checker() {
  const capabilities = useCapabilities();
  const [skills, setSkills] = useState<SkillItem[]>([]);
  const [patterns, setPatterns] = useState<PatternItem[]>([]);
  const [result, setResult] = useState<{
    response: LintResponse;
    text: string;
    requestId: number;
  } | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [metadataUnavailable, setMetadataUnavailable] = useState(false);
  const requestGeneration = useRef(0);

  useEffect(() => {
    let active = true;
    Promise.all([fetchSkills(), fetchPatterns()])
      .then(([skillsRes, patternsRes]) => {
        if (!active) return;
        setSkills(skillsRes.skills);
        setPatterns(patternsRes.patterns);
      })
      .catch(() => {
        if (active) setMetadataUnavailable(true);
      });
    return () => {
      active = false;
      requestGeneration.current += 1;
    };
  }, []);

  const invalidateResult = () => {
    requestGeneration.current += 1;
    setResult(null);
    setErrorMsg(null);
    setLoading(false);
  };
  const handleLint = async (text: string, selectedSkills: string[]) => {
    const requestId = ++requestGeneration.current;
    setLoading(true);
    setErrorMsg(null);
    setResult(null);
    try {
      const response = await lintText(text, selectedSkills);
      if (requestId !== requestGeneration.current) return;
      setResult({ response, text, requestId });
    } catch (error: unknown) {
      if (requestId !== requestGeneration.current) return;
      setErrorMsg(
        error instanceof TypeError
          ? "Chưa kết nối được máy chủ. Bạn hãy thử lại sau."
          : error instanceof Error
            ? error.message
            : "Chưa kiểm tra được văn bản. Bạn hãy thử lại.",
      );
    } finally {
      if (requestId === requestGeneration.current) setLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      <header className={styles.heading}>
        <div>
          <h1>Soát văn phong tiếng Việt</h1>
          <p>Tìm chỗ cần đọc lại, hiểu lý do và tự chọn cách sửa phù hợp.</p>
        </div>
        {capabilities.contributions && (
          <Link href="/contribute" className="text-link action-link">
            Góp mẫu văn bản
          </Link>
        )}
      </header>
      <p aria-live="polite" aria-atomic="true" className="sr-only">
        {loading
          ? "Đang kiểm tra văn bản. Vui lòng chờ kết quả."
          : result
            ? `Đã kiểm tra. Có ${result.response.summary.total} mục cần cân nhắc.`
            : ""}
      </p>
      <div className={styles.workbench}>
        <div className={styles.checkColumns}>
          <Editor
            skills={skills}
            onLint={handleLint}
            loading={loading}
            onTextChange={invalidateResult}
            onSkillsChange={invalidateResult}
          />
          <div className={styles.review}>
            {errorMsg ? (
              <section role="alert" className={styles.resultState}>
                <div className={styles.toolbar}>
                  <h2 className={styles.danger}>Chưa kiểm tra được văn bản</h2>
                </div>
                <p>{errorMsg}</p>
                <p>
                  Văn bản của bạn vẫn được giữ trong ô nhập. Bấm “Soát văn
                  phong” để thử lại.
                </p>
                <Link href="/start" className="text-link action-link">
                  Dùng trong chatbot
                </Link>
              </section>
            ) : loading ? (
              <section
                aria-busy="true"
                aria-label="Đang soát văn bản"
                className={styles.resultState}
              >
                <div className={styles.toolbar}>
                  <h2>Đang kiểm tra văn bản…</h2>
                </div>
                <p>Đang đối chiếu với các nhóm quy tắc bạn đã chọn.</p>
                <div aria-hidden="true" className={styles.skeleton}>
                  {[0, 1, 2].map((item) => (
                    <div key={item} className={styles.skeletonItem}>
                      <div className={styles.skeletonLine} />
                      <div className={styles.skeletonLine} />
                      <div className={styles.skeletonLine} />
                    </div>
                  ))}
                </div>
              </section>
            ) : result ? (
              <IssueList
                key={`findings-${result.requestId}`}
                summary={result.response.summary}
                issues={result.response.issues}
                patterns={patterns}
              />
            ) : (
              <section
                className={styles.resultState}
                aria-labelledby="results-title"
              >
                <div className={styles.toolbar}>
                  <h2 id="results-title">Kết quả soát văn phong</h2>
                </div>
                <div className={styles.emptyContent}>
                  <h3>Bắt đầu từ một đoạn bạn đang viết.</h3>
                  <p>
                    Dán văn bản rồi bấm “Soát văn phong”. Bạn cũng có thể thử
                    văn bản mẫu để xem cách đọc kết quả.
                  </p>
                </div>
              </section>
            )}
            {metadataUnavailable && !errorMsg && (
              <p role="status" className={`${styles.notice} ${styles.warning}`}>
                Phần giải thích quy tắc chưa tải được.
              </p>
            )}
          </div>
        </div>
        {result && capabilities.rewrite && (
          <RewritePanel
            key={`rewrite-${result.requestId}`}
            originalText={result.text}
            issueIds={result.response.issues.map((issue) => issue.pattern_id)}
          />
        )}
      </div>
    </div>
  );
}
