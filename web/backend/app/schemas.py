from typing import Literal

from pydantic import BaseModel, Field

VALID_SKILLS = {
    "humanizer-vi",
    "translationese-cleaner-vi",
    "grammar-checker-vi",
    "style-guide-vi",
}


class LintRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
    skills: list[str] | None = None


class IssueOccurrence(BaseModel):
    line: int
    column: int
    excerpt: str
    matched_text: str


class IssueItem(BaseModel):
    pattern_id: str
    finding_type: str
    severity: str
    confidence: str
    scope: str
    line: int
    column: int
    excerpt: str
    message: str
    suggestion: str
    occurrences: list[IssueOccurrence]


class LintSummary(BaseModel):
    total: int
    error: int
    warning: int
    preference: int
    heuristic: int
    note: str = (
        "Các mục dưới đây cần bạn xem lại theo ngữ cảnh; "
        "số lượng không cho biết văn bản do ai viết."
    )


class LintResponse(BaseModel):
    version: str
    summary: LintSummary
    issues: list[IssueItem]


class PatternItem(BaseModel):
    id: str
    name: str
    skill: str
    category: str
    finding_type: str
    severity: str
    summary: str
    why_it_matters: str
    rewrite_strategy: str


class PatternsResponse(BaseModel):
    patterns: list[PatternItem]


class SkillItem(BaseModel):
    id: str
    name: str
    when_to_use: str
    when_not_to_use: str


class SkillsResponse(BaseModel):
    skills: list[SkillItem]


OutputMode = Literal["clean_rewrite", "review_comment", "needs_author_decision", "no_change"]


class RewriteStyle(BaseModel):
    profile: Literal[
        "preserve", "plain", "business", "technical", "administrative", "social", "marketing"
    ] = "preserve"
    channel: Literal["auto", "document", "email", "chat", "spoken_script"] = "auto"
    register_name: Literal["preserve", "formal", "professional", "friendly", "conversational"] = (
        Field("preserve", alias="register")
    )
    audience: str = Field("", max_length=300)
    relationship: str = Field("", max_length=300)
    pronouns: str = Field("", max_length=200)
    edit_level: Literal["light", "moderate", "deep"] = "light"
    reduce_hype: bool = False


class RewriteRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
    skill: str = "humanizer-vi"
    issue_ids: list[str] | None = None
    context: str = Field("", max_length=5000)
    style: RewriteStyle = Field(default_factory=RewriteStyle)


class RewriteResponse(BaseModel):
    rewrite: str
    output_mode: OutputMode = "clean_rewrite"
    comments: list[str] = Field(default_factory=list)
    review_status: str = "unreviewed"
    disclaimer: str = "Gợi ý do AI tạo. Hãy đối chiếu với bản gốc để kiểm tra dữ kiện và ý nghĩa."


class ContributionCreate(BaseModel):
    input_text: str = Field(..., min_length=1, max_length=20000)
    context: str | None = Field(None, max_length=5000)
    suggestion: str = Field(..., min_length=1, max_length=20000)
    skill: str = "humanizer-vi"
    pattern_ids: list[str] | None = None
    note: str | None = Field(None, max_length=5000)
    consent: bool


class ContributionResponse(BaseModel):
    id: str
    status: str
    message: str


class AdminContributionItem(BaseModel):
    id: str
    created_at: str
    input_text: str
    context: str | None = None
    suggestion: str
    skill: str
    pattern_ids: list[str] | None = None
    note: str | None = None
    consent: bool
    status: str
    review_note: str | None = None
    reviewed_at: str | None = None


class AdminContributionPatch(BaseModel):
    status: str
    review_note: str | None = None
