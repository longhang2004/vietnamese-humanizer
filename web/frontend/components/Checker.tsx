"use client";

import React, { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useCapabilities } from "./CapabilityNav";
import { Editor } from "./Editor";
import { IssueList } from "./IssueList";
import { RewritePanel } from "./RewritePanel";
import { fetchPatterns, fetchSkills, lintText } from "../lib/api";
import type { LintResponse, PatternItem, SkillItem } from "../lib/types";

export function Checker() {
  const capabilities = useCapabilities();
  const [skills, setSkills] = useState<SkillItem[]>([]);
  const [patterns, setPatterns] = useState<PatternItem[]>([]);
  const [result, setResult] = useState<{ response: LintResponse; text: string; requestId: number } | null>(null);
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
      .catch(() => { if (active) setMetadataUnavailable(true); });
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
      setErrorMsg(error instanceof Error ? error.message : "Chưa kiểm tra được văn bản. Bạn hãy thử lại.");
    } finally {
      if (requestId === requestGeneration.current) setLoading(false);
    }
  };

  return (
    <div className="space-y-7 py-12">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div className="max-w-2xl">
          <h1 className="text-3xl font-semibold tracking-tight">Soát văn phong tiếng Việt</h1>
          <p className="mt-3 text-base leading-7 text-[var(--muted)]">Tìm chỗ cần đọc lại, hiểu lý do và tự chọn cách sửa phù hợp.</p>
        </div>
        <div className="flex flex-wrap items-center gap-5"><Link href="/start" className="text-link inline-flex min-h-11 items-center text-sm">Dùng trong chatbot</Link>{capabilities.contributions && <Link href="/contribute" className="text-link inline-flex min-h-11 items-center text-sm">Góp mẫu văn bản</Link>}</div>
      </div>

      {metadataUnavailable && <p role="status" className="text-sm leading-6 text-[var(--warning)]">Chưa tải được phần giải thích quy tắc. Bạn vẫn có thể chọn nhóm kiểm tra và thử soát văn bản.</p>}

      <div className="grid grid-cols-1 items-start gap-6 lg:grid-cols-2">
        <Editor skills={skills} onLint={handleLint} loading={loading} onTextChange={invalidateResult} onSkillsChange={invalidateResult} />
        <div className="min-w-0 space-y-6">
          <p aria-live="polite" aria-atomic="true" className="sr-only">{loading ? "Đang kiểm tra văn bản. Vui lòng chờ kết quả." : result ? `Đã kiểm tra. Có ${result.response.summary.total} mục cần cân nhắc.` : ""}</p>

          {errorMsg ? (
            <section role="alert" className="surface-panel p-5 sm:p-6">
              <h2 className="text-xl font-semibold text-[var(--danger)]">Chưa kiểm tra được văn bản</h2>
              <p className="mt-3 break-words text-base leading-7">{errorMsg}</p>
              <p className="mt-3 text-base leading-7 text-[var(--muted)]">Văn bản của bạn vẫn được giữ trong ô nhập. Bấm “Soát văn phong” để thử lại.</p>
            </section>
          ) : loading ? (
            <section aria-busy="true" aria-label="Đang soát văn bản" className="surface-panel min-h-[26rem] p-5 sm:p-6">
              <h2 className="text-xl font-semibold">Đang kiểm tra văn bản…</h2>
              <p className="mt-3 text-base leading-7 text-[var(--muted)]">Đang đối chiếu với các nhóm quy tắc bạn đã chọn.</p>
              <div aria-hidden="true" className="mt-8 space-y-5">
                {[0, 1, 2].map((item) => <div key={item} className="space-y-3 border-t border-[var(--border)] pt-5"><div className="h-4 w-2/5 rounded bg-[var(--surface-raised)]" /><div className="h-4 w-full rounded bg-[var(--surface-raised)]" /><div className="h-4 w-4/5 rounded bg-[var(--surface-raised)]" /></div>)}
              </div>
            </section>
          ) : result ? (
            <IssueList key={`findings-${result.requestId}`} summary={result.response.summary} issues={result.response.issues} patterns={patterns} />
          ) : (
            <section className="surface-panel flex min-h-[26rem] flex-col p-5 sm:p-6" aria-labelledby="results-title">
              <h2 id="results-title" className="text-xl font-semibold">Kết quả soát văn phong</h2>
              <div className="my-auto py-12">
                <h3 className="text-lg font-medium">Bắt đầu từ một đoạn bạn đang viết.</h3>
                <p className="mt-3 max-w-prose text-base leading-7 text-[var(--muted)]">Dán văn bản, chọn nhóm kiểm tra rồi bấm “Soát văn phong”. Hoặc thử văn bản mẫu để xem cách đọc kết quả.</p>

              </div>
            </section>
          )}

          {result && capabilities.rewrite && <RewritePanel key={`rewrite-${result.requestId}`} originalText={result.text} issueIds={result.response.issues.map((issue) => issue.pattern_id)} />}
        </div>
      </div>
    </div>
  );
}
