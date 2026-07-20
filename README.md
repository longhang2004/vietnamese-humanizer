# Vietnamese Writing Skills

Bộ công cụ biên tập tiếng Việt giúp văn bản rõ ràng, tự nhiên, nhất quán và phù hợp với ngữ cảnh.

Repository gồm bốn Agent Skills và một lớp công cụ deterministic để kiểm cấu trúc, quản lý pattern, lint tín hiệu bề mặt và chạy benchmark. Dự án không phân loại văn bản do người hay AI viết, không tạo "AI probability score" và không hướng dẫn vượt detector.

## Dự án giải quyết gì

Văn bản tiếng Việt có thể đúng ngữ pháp nhưng vẫn khó đọc vì danh hóa dày, cấu trúc dịch sát tiếng Anh, giọng lệch đối tượng hoặc trình bày thiếu nhất quán. Các skill hỗ trợ reviewer xử lý những vấn đề đó mà không làm mất dữ kiện, số liệu, tên riêng, thuật ngữ, điều kiện và mức chắc chắn.

## Bốn skill

| Skill | Dùng khi | Không dùng khi |
| --- | --- | --- |
| `humanizer-vi` | Văn bản khuôn mẫu, sáo, đều nhịp hoặc lệch giọng | Suy đoán tác giả, lách detector, soát lỗi thuần cơ học |
| `translationese-cleaner-vi` | Câu tiếng Việt bám trật tự, ẩn dụ hoặc danh hóa tiếng Anh | Tự thay thuật ngữ chuẩn hay làm yếu văn bản pháp lý |
| `grammar-checker-vi` | Soát chính tả, dấu câu, cấu trúc và mơ hồ | Áp một phong cách hoặc sửa code, URL, identifier |
| `style-guide-vi` | Giữ nhất quán xưng hô, thuật ngữ, số và định dạng | Ghi đè style guide riêng hoặc đổi dữ kiện |

## Ví dụ

Input:

> Trong bài viết này, chúng ta sẽ cùng khám phá cách Redis giúp tối ưu hiệu suất.

Output:

> Redis giữ dữ liệu thường dùng trong bộ nhớ để giảm số lần đọc từ nguồn chậm hơn.

Skill bỏ câu thông báo và đi thẳng vào cơ chế. Nếu input đã rõ, chẳng hạn "API có thể trả lỗi 429 nếu client gửi quá 100 yêu cầu mỗi phút", skill nên giữ nguyên.

## Cài đặt

### Dùng Agent Skills

Clone repository rồi trỏ agent tương thích Agent Skills đến từng thư mục trong `skills/`, hoặc sao chép skill cần dùng vào thư mục skill của agent. Mỗi thư mục tự chứa `SKILL.md`, README và references.

```bash
git clone https://github.com/your-org/vietnamese-writing-skills.git
```

URL trên là ví dụ cho repository sau khi được publish. Khi làm việc từ bản clone hiện tại, dùng trực tiếp đường dẫn `skills/humanizer-vi` và các thư mục cùng cấp.

### Dùng công cụ Python

Yêu cầu Python 3.11 trở lên.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Cách dùng

Yêu cầu trực tiếp với agent:

```text
Dùng humanizer-vi để biên tập email này. Giữ giọng chuyên nghiệp,
mọi con số, tên sản phẩm và hạn chót.
```

Lint một file hoặc thư mục:

```bash
python scripts/lint_vietnamese.py article.md
python scripts/lint_vietnamese.py article.md --format json
python scripts/lint_vietnamese.py docs/ --recursive
python scripts/lint_vietnamese.py article.md --skill humanizer-vi
```

Linter chỉ trả số tín hiệu cần review. Exit code `1` nghĩa là có tín hiệu, không phải văn bản "do AI viết" và cũng không khẳng định có lỗi.

## Kiểm tra repository

```bash
ruff check .
pytest
python scripts/validate_skills.py
python scripts/validate_patterns.py
python scripts/run_benchmarks.py --validate-only
python scripts/generate_pattern_docs.py --check
```

Sinh lại bảng pattern sau khi sửa YAML:

```bash
python scripts/generate_pattern_docs.py
```

## Dữ liệu và benchmark

- 40 pattern trong `patterns/`, mỗi pattern có tín hiệu, hai ví dụ xấu, hai ví dụ tốt, ngoại lệ và rủi ro false positive.
- 100 cặp trước/sau có metadata trong `examples/examples.jsonl`.
- 30 benchmark case trong `benchmarks/cases/`, chấm theo tám tiêu chí từ 1 đến 5.
- Unit test chỉ kiểm phần deterministic. Bản sửa ngôn ngữ cần reviewer bản ngữ.

## Đóng góp pattern

Đọc [CONTRIBUTING.md](CONTRIBUTING.md) và [hướng dẫn viết pattern](docs/pattern-authoring-guide.md). Một pattern mới cần bằng chứng quan sát, ít nhất hai ví dụ ở ngữ cảnh khác nhau, ngoại lệ, rủi ro false positive và test hoặc benchmark case. Không merge danh sách từ cấm thiếu ngữ cảnh.

## Triết lý thiết kế

- Chất lượng biên tập quan trọng hơn việc đoán nguồn gốc văn bản.
- Bảo toàn nội dung là ràng buộc, không phải điểm cộng tùy chọn.
- Pattern là tín hiệu review theo mật độ và ngữ cảnh, không phải lỗi tự động.
- Logic ngôn ngữ nằm trong Agent Skills; CLI chỉ phát hiện phần bề mặt có thể kiểm tra ổn định.
- Tiếng Việt có khác biệt vùng miền, thế hệ, nghề nghiệp và register. Dự án không chọn một nhóm làm chuẩn duy nhất.

## Giới hạn

MVP dùng rule bề mặt, chưa có corpus gán nhãn riêng và chưa được đánh giá liên chủ thể trên quy mô lớn. Regex có thể bỏ sót biến thể hoặc báo nhầm thuật ngữ ngành. Xem [limitations](docs/limitations.md) và [research notes](docs/research-notes.md).

## Attribution

Dự án tham khảo định dạng [Agent Skills](https://agentskills.io/specification), ý tưởng audit văn phong của [blader/humanizer](https://github.com/blader/humanizer) và kinh nghiệm bản địa hóa từ các dự án tiếng Trung, tiếng Hàn. Taxonomy, ví dụ và corpus tiếng Việt trong repository được viết riêng, không phải bản dịch từng dòng. Chi tiết license và bài nghiên cứu nằm trong [research notes](docs/research-notes.md).

## Roadmap và license

Xem [ROADMAP.md](ROADMAP.md). Mã và nội dung gốc của repository được phát hành theo [MIT License](LICENSE).
