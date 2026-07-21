import {
  ContributionRequest,
  ContributionResponse,
  LintResponse,
  PatternsResponse,
  RewriteResponse,
  SkillsResponse,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorDetail = `Yêu cầu thất bại với mã lỗi HTTP ${res.status}`;
    try {
      const data = await res.json();
      if (data.detail) {
        errorDetail = data.detail;
      }
    } catch {
      // JSON parse error fallback
    }
    throw new Error(errorDetail);
  }
  return res.json();
}

export async function lintText(text: string, skills?: string[]): Promise<LintResponse> {
  const res = await fetch(`${API_BASE}/api/lint`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, skills }),
  });
  return handleResponse<LintResponse>(res);
}

export async function fetchPatterns(): Promise<PatternsResponse> {
  const res = await fetch(`${API_BASE}/api/patterns`);
  return handleResponse<PatternsResponse>(res);
}

export async function fetchSkills(): Promise<SkillsResponse> {
  const res = await fetch(`${API_BASE}/api/skills`);
  return handleResponse<SkillsResponse>(res);
}

export async function rewriteText(
  text: string,
  skill: string = "humanizer-vi",
  issueIds?: string[]
): Promise<RewriteResponse> {
  const res = await fetch(`${API_BASE}/api/rewrite`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, skill, issue_ids: issueIds }),
  });
  return handleResponse<RewriteResponse>(res);
}

export async function submitContribution(
  data: ContributionRequest
): Promise<ContributionResponse> {
  const res = await fetch(`${API_BASE}/api/contributions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse<ContributionResponse>(res);
}
