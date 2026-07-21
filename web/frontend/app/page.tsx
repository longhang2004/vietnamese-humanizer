"use client";

import React, { useEffect, useState } from "react";
import { Disclaimer } from "../components/Disclaimer";
import { Editor } from "../components/Editor";
import { IssueList } from "../components/IssueList";
import { RewritePanel } from "../components/RewritePanel";
import { fetchPatterns, fetchSkills, lintText } from "../lib/api";
import { LintResponse, PatternItem, SkillItem } from "../lib/types";

export default function HomePage() {
  const [skills, setSkills] = useState<SkillItem[]>([]);
  const [patterns, setPatterns] = useState<PatternItem[]>([]);
  const [currentText, setCurrentText] = useState<string>("");
  const [lintResult, setLintResult] = useState<LintResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    async function loadMetadata() {
      try {
        const [skillsRes, patternsRes] = await Promise.all([fetchSkills(), fetchPatterns()]);
        setSkills(skillsRes.skills);
        setPatterns(patternsRes.patterns);
      } catch (err: unknown) {
        console.error("Failed to load metadata:", err);
      }
    }
    loadMetadata();
  }, []);

  const handleLint = async (text: string, selectedSkills: string[]) => {
    setCurrentText(text);
    setLoading(true);
    setErrorMsg(null);
    try {
      const res = await lintText(text, selectedSkills);
      setLintResult(res);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg("Đã xảy ra lỗi không xác định khi kiểm tra văn bản.");
      }
      setLintResult(null);
    } finally {
      setLoading(false);
    }
  };

  const detectedPatternIds = lintResult?.issues.map((i) => i.pattern_id);

  return (
    <div>
      <Disclaimer />

      <Editor skills={skills} onLint={handleLint} loading={loading} />

      {errorMsg && (
        <div className="bg-red-50 border border-red-200 text-red-900 p-4 rounded-lg text-sm mb-6">
          <p className="font-bold">❌ Lỗi kiểm tra văn phong:</p>
          <p className="mt-1">{errorMsg}</p>
        </div>
      )}

      {lintResult && (
        <>
          <IssueList
            summary={lintResult.summary}
            issues={lintResult.issues}
            patterns={patterns}
          />

          <RewritePanel
            originalText={currentText}
            issueIds={detectedPatternIds}
          />
        </>
      )}
    </div>
  );
}
