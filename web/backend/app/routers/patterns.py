from fastapi import APIRouter, Request

from app.limiter import limiter
from app.schemas import PatternsResponse, SkillItem, SkillsResponse
from app.services.linter import get_patterns_list

router = APIRouter(prefix="/api", tags=["Metadata"])

SKILLS_DATA = [
    SkillItem(
        id="humanizer-vi",
        name="Viết tự nhiên hơn",
        when_to_use="Sửa câu sáo rỗng, máy móc hoặc lệch giọng; giữ dữ kiện và giọng tác giả.",
        when_not_to_use=(
            "Đoán ai viết văn bản, vượt công cụ phát hiện AI hoặc chỉ soát lỗi chính tả."
        ),
    ),
    SkillItem(
        id="translationese-cleaner-vi",
        name="Sửa câu dịch chưa tự nhiên",
        when_to_use=(
            "Sửa câu tiếng Việt dịch sát cấu trúc tiếng Anh; giữ thuật ngữ và ý nghĩa bản gốc."
        ),
        when_not_to_use="Soát lỗi chính tả đơn thuần hoặc sửa văn bản đã tự nhiên",
    ),
    SkillItem(
        id="grammar-checker-vi",
        name="Soát lỗi tiếng Việt",
        when_to_use="Kiểm tra chính tả, dấu câu, cấu trúc câu và chỗ mơ hồ trong tiếng Việt.",
        when_not_to_use="Đánh giá bài viết hay hay dở hoặc kết luận văn bản do AI tạo.",
    ),
    SkillItem(
        id="style-guide-vi",
        name="Giữ cách viết nhất quán",
        when_to_use=(
            "Thống nhất cách xưng hô, thuật ngữ, viết hoa, số, ngày giờ, đơn vị và định dạng."
        ),
        when_not_to_use="Áp một quy ước chung thay cho quy ước riêng bạn đã cung cấp.",
    ),
]


@router.get("/patterns", response_model=PatternsResponse)
@limiter.limit("60/minute")
def get_patterns_endpoint(request: Request):
    return PatternsResponse(patterns=get_patterns_list())


@router.get("/skills", response_model=SkillsResponse)
@limiter.limit("60/minute")
def get_skills_endpoint(request: Request):
    return SkillsResponse(skills=SKILLS_DATA)
