"use client";

import { useState } from "react";
import { REPOSITORY_URL } from "../lib/repository";
import { Icon } from "./Icon";

export interface ComparisonCase {
  id: string; topic: string; tone: string; profile: string;
  prompt: string; input: string; without: string; with: string;
}

export function ComparisonExplorer({ cases, initialId }: { cases: ComparisonCase[]; initialId?: string }) {
  const [selectedId, setSelectedId] = useState(initialId ?? cases[0].id);
  const selected = cases.find((item) => item.id === selectedId) ?? cases[0];
  const index = cases.indexOf(selected);
  return <div className="comparison-explorer">
    <div className="comparison-toolbar">
      <div className="comparison-select"><label htmlFor="comparison-topic" className="field-label">Chủ đề so sánh</label><select className="field" id="comparison-topic" value={selected.id} onChange={(event) => setSelectedId(event.target.value)}>{cases.map((item) => <option key={item.id} value={item.id}>{item.topic}</option>)}</select></div>
      <p className="comparison-tone">{selected.tone}</p>
      <div className="comparison-stepper"><span>{index + 1} / {cases.length}</span><button type="button" className="button-icon" aria-label="Chủ đề trước" onClick={() => setSelectedId(cases[(index + cases.length - 1) % cases.length].id)}><Icon name="arrow" className="rotate-180" /></button><button type="button" className="button-icon" aria-label="Chủ đề tiếp theo" onClick={() => setSelectedId(cases[(index + 1) % cases.length].id)}><Icon name="arrow" /></button></div>
    </div>
    <div className="comparison-columns" aria-live="polite" aria-atomic="true">
      <section className="comparison-output" aria-label="Kết quả AI không nạp skill"><h3>AI không nạp skill</h3><p>{selected.without}</p></section>
      <section className="comparison-output guided-output" aria-label="Kết quả AI có nạp skill"><h3><Icon name="book" width="17" height="17" />AI có nạp skill</h3><p>{selected.with}</p></section>
    </div>
    <details className="comparison-source" key={selected.id}>
      <summary>Xem yêu cầu và đoạn gốc</summary><div className="source-content"><h4>Yêu cầu dùng cho cả hai lượt</h4><p>{selected.prompt}</p><h4>Đoạn gốc</h4><p className="whitespace-pre-wrap">{selected.input}</p></div>
    </details>
    <div className="comparison-provenance"><p>Đầu ra AI được giữ nguyên văn từ các lượt chạy ngày 04/11/2026.</p><a href={`${REPOSITORY_URL}/tree/main/docs/research/2026-11-04-web-comparisons`} target="_blank" rel="noopener noreferrer">Xem bản ghi gốc <Icon name="external" width="14" height="14" /></a></div>
  </div>;
}
