export interface IssueOccurrence {
  line: number;
  column: number;
  excerpt: string;
  matched_text: string;
}

export interface IssueItem {
  pattern_id: string;
  finding_type: "error" | "warning" | "preference" | "heuristic" | string;
  severity: "high" | "medium" | "low" | string;
  confidence: string;
  scope: string;
  line: number;
  column: number;
  excerpt: string;
  message: string;
  suggestion: string;
  occurrences: IssueOccurrence[];
}

export interface LintSummary {
  total: number;
  error: number;
  warning: number;
  preference: number;
  heuristic: number;
  note: string;
}

export interface LintResponse {
  version: string;
  summary: LintSummary;
  issues: IssueItem[];
}

export interface HealthResponse {
  status: string;
  version: string;
  capabilities: {
    rewrite: boolean;
    contributions: boolean;
  };
}

export interface PatternItem {
  id: string;
  name: string;
  skill: string;
  category: string;
  finding_type: string;
  severity: string;
  summary: string;
  why_it_matters: string;
  rewrite_strategy: string;
}

export interface PatternsResponse {
  patterns: PatternItem[];
}

export interface SkillItem {
  id: string;
  name: string;
  when_to_use: string;
  when_not_to_use: string;
}

export interface SkillsResponse {
  skills: SkillItem[];
}

export interface RewriteResponse {
  rewrite: string;
  review_status: string;
  disclaimer: string;
}

export interface ContributionRequest {
  input_text: string;
  context?: string;
  suggestion: string;
  skill: string;
  pattern_ids?: string[];
  note?: string;
  consent: boolean;
}

export interface ContributionResponse {
  id: string;
  status: string;
  message: string;
}
