from fastapi import APIRouter, Request

from app.limiter import limiter
from app.schemas import PatternsResponse, SkillItem, SkillsResponse
from app.services.linter import get_patterns_list

router = APIRouter(prefix="/api", tags=["Metadata"])

SKILLS_DATA = [
    SkillItem(
        id="humanizer-vi",
        name="Humanizer tiếng Việt",
        when_to_use="Văn bản có vẻ theo khuôn, sáo, đều nhịp hoặc lệch giọng",
        when_not_to_use="Suy đoán tác giả, lách detector, hoặc chỉ soát lỗi máy móc",
    ),
    SkillItem(
        id="translationese-cleaner-vi",
        name="Gọt dịch thuật ngữ tiếng Việt",
        when_to_use="Văn bản dịch thô, câu bị động khiên cưỡng, lạm dụng cấu trúc dịch tiếng Anh",
        when_not_to_use="Soát lỗi chính tả đơn thuần hoặc sửa văn bản đã tự nhiên",
    ),
    SkillItem(
        id="grammar-checker-vi",
        name="Soát lỗi ngữ pháp & chính tả tiếng Việt",
        when_to_use="Phát hiện lỗi sai từ ngữ, sai ngữ pháp, câu thiếu chủ/vị rõ ràng",
        when_not_to_use="Đánh giá văn phong hay/dở hoặc quy kết văn bản do AI sinh",
    ),
    SkillItem(
        id="style-guide-vi",
        name="Quy chuẩn văn phong & báo chí",
        when_to_use="Rà soát tính nhất quán về thuật ngữ, xưng hô, định dạng và hành văn chuyên nghiệp",
        when_not_to_use="Sáng tạo nghệ thuật tự do hoặc thay thế quy chuẩn riêng của tòa soạn",
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
