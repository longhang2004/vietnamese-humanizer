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
    <div className="space-y-6">
      {/* Top Banner Disclaimer */}
      <Disclaimer />

      {/* Main Workspace */}
      <div className="grid grid-cols-1 gap-6">
        <Editor skills={skills} onLint={handleLint} loading={loading} />

        {errorMsg && (
          <div className="bg-rose-50 border border-rose-200/80 text-rose-950 p-4 rounded-xl text-xs sm:text-sm flex items-start space-x-3 shadow-sm">
            <div className="flex-shrink-0 w-6 h-6 text-rose-600 mt-0.5">
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
              </svg>
            </div>
            <div>
              <p className="font-bold text-rose-950">Lỗi kiểm tra văn phong:</p>
              <p className="mt-0.5 text-rose-800 leading-relaxed">{errorMsg}</p>
            </div>
          </div>
        )}

        {lintResult && (
          <div className="space-y-8 animate-in fade-in duration-300">
            <IssueList
              summary={lintResult.summary}
              issues={lintResult.issues}
              patterns={patterns}
            />

            <RewritePanel
              originalText={currentText}
              issueIds={detectedPatternIds}
            />
          </div>
        )}
      </div>
    </div>
  );
}

