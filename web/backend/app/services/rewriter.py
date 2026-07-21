from google import genai
from google.genai import types
from vietnamese_writing_skills.cli.lint import lint_text
from vietnamese_writing_skills.core.paths import data_location
from vietnamese_writing_skills.core.patterns import pattern_index

from app.config import settings
from app.schemas import RewriteResponse


class GeminiKeyMissingError(Exception):
    """Raised when GEMINI_API_KEY is not configured."""


def generate_rewrite(text: str, skill: str = "humanizer-vi", issue_ids: list[str] | None = None) -> RewriteResponse:
    if not settings.GEMINI_API_KEY:
        raise GeminiKeyMissingError("GEMINI_API_KEY is not configured on the backend server.")

    # 1. Lint text to get actual issues
    raw_issues = lint_text(text, skills={skill})
    if issue_ids:
        raw_issues = [i for i in raw_issues if i["pattern_id"] in issue_ids]

    # 2. Read SKILL.md
    skills_path = data_location("skills")
    skill_md_path = skills_path / skill / "SKILL.md"
    skill_content = ""
    if hasattr(skill_md_path, "read_text"):
        try:
            skill_content = skill_md_path.read_text(encoding="utf-8")
        except Exception:
            skill_content = ""

    # 3. Retrieve relevant pattern rewrite strategies
    all_patterns = pattern_index()
    strategies = []
    for issue in raw_issues:
        pid = issue["pattern_id"]
        if pid in all_patterns:
            pat = all_patterns[pid]
            strat = pat.get("rewrite_strategy", [])
            strategies.append(f"- Pattern {pid}: {strat}")

    strategies_text = "\n".join(strategies) if strategies else "None specified."

    # 4. Construct prompt and system instruction
    system_instruction = (
        "Bạn là biên tập viên tiếng Việt. Sửa văn bản theo hướng dẫn skill và danh sách issue, "
        "nhưng BẮT BUỘC bảo toàn: dữ kiện, số liệu, tên riêng, mức độ chắc chắn, thuật ngữ chuyên môn. "
        "Không thêm ví dụ/nguồn/metric mới. Trả lại chỉ văn bản đã sửa, không giải thích."
    )

    user_prompt = f"""\
[Skill Guidelines]
{skill_content[:2000]}

[Detected Issues & Strategies]
{strategies_text}

[Original Text]
{text}
"""

    # 5. Call Gemini API using google-genai SDK
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = None
    for model_name in ["gemini-2.5-flash", "gemini-2.0-flash"]:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3,
                ),
            )
            if response and response.text:
                break
        except Exception as e:
            if model_name == "gemini-2.0-flash":
                raise e

    rewrite_text = response.text.strip() if response.text else text

    return RewriteResponse(
        rewrite=rewrite_text,
        review_status="unreviewed",
        disclaimer="Gợi ý do model sinh, cần người đọc kiểm chứng bảo toàn dữ kiện.",
    )
