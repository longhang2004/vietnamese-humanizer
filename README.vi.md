[English](README.md) | **Tiếng Việt**

# Vietnamese Writing Skills

[![CI](https://github.com/longhang2004/vietnamese-humanizer/actions/workflows/ci.yml/badge.svg)](https://github.com/longhang2004/vietnamese-humanizer/actions/workflows/ci.yml)
[![Python 3.11–3.14](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Bộ công cụ biên tập tiếng Việt giúp văn bản rõ, tự nhiên, nhất quán và phù hợp ngữ cảnh mà không làm mất dữ kiện.

Repository vẫn mang tên `vietnamese-humanizer` vì đó là URL dự án. Sản phẩm có tên **Vietnamese Writing Skills** vì gồm bốn skill, không chỉ humanizer. Bản phân phối Python dùng tên `vietnamese-writing-skills`, còn package để import là `vietnamese_writing_skills`.

Dự án không phân loại tác giả, không tạo “AI probability score” và không hướng dẫn vượt detector. Linter chỉ tìm tín hiệu bề mặt để con người review.

## Bốn skill

| Skill | Dùng khi | Không dùng khi |
| --- | --- | --- |
| `humanizer-vi` | Văn bản khuôn mẫu, sáo, đều nhịp hoặc lệch giọng | Suy đoán tác giả, lách detector, soát lỗi thuần cơ học |
| `translationese-cleaner-vi` | Câu tiếng Việt bám trật tự, ẩn dụ hoặc danh hóa tiếng Anh | Tự thay thuật ngữ chuẩn hay làm yếu văn bản pháp lý |
| `grammar-checker-vi` | Soát chính tả, dấu câu, cấu trúc và mơ hồ | Áp một phong cách hoặc sửa code, URL, identifier |
| `style-guide-vi` | Giữ nhất quán xưng hô, thuật ngữ, số và định dạng | Ghi đè style guide riêng hoặc đổi dữ kiện |

## Ví dụ bảo toàn dữ kiện

Trước:

> Trong bài viết này, chúng ta sẽ cùng tìm hiểu cách Redis lưu dữ liệu thường dùng trong bộ nhớ để giảm số lần truy cập nguồn dữ liệu chậm hơn.

Sau:

> Redis lưu dữ liệu thường dùng trong bộ nhớ, nhờ đó hệ thống ít phải truy cập nguồn dữ liệu chậm hơn.

Bản sửa chỉ bỏ câu thông báo. Cơ chế Redis đã có trong input, không được suy ra từ một câu chung như “Redis giúp tối ưu hiệu suất”. Với corpus, thông tin nằm ngoài input phải được ghi rõ trong trường `context`.

## Bốn output mode

- `clean_rewrite`: Bản viết lại có thể thay trực tiếp cho input và giữ nguyên ý.
- `review_comment`: Nhận xét cho người viết khi thiếu nguồn hoặc bằng chứng; đây không phải replacement text.
- `needs_author_decision`: Có nhiều cách hiểu nên cần người viết xác nhận trước khi sửa.
- `no_change`: Input đã ổn; không sửa chỉ để tạo khác biệt.

Agent không bị buộc phải rewrite mọi input. Từ chối đoán là hành vi đúng khi chủ thể, phạm vi, ngày tháng hoặc mức độ nghĩa vụ còn mơ hồ.

## Cài Agent Skills từ repository

```bash
git clone https://github.com/longhang2004/vietnamese-humanizer.git
cd vietnamese-humanizer
```

Trỏ agent tương thích Agent Skills đến thư mục cần dùng trong `skills/`, hoặc sao chép riêng thư mục đó vào nơi agent đọc skill. Mỗi skill chứa `SKILL.md`, tài liệu tham chiếu và tài sản cần thiết.

Ví dụ yêu cầu:

```text
Dùng humanizer-vi để biên tập email này. Giữ giọng chuyên nghiệp,
mọi con số, tên sản phẩm, điều kiện và hạn chót.
```

## Cài Python CLI

Yêu cầu Python 3.11 trở lên. Cài trực tiếp từ source checkout:

```bash
python -m pip install .
```

Build và cài wheel:

```bash
python -m pip install build
python -m build
python -m pip install dist/*.whl
```

Cài cho phát triển:

```bash
python -m pip install -e ".[dev]"
```

Wheel chứa pattern, schema, skill Markdown, example và benchmark resources. CLI mặc định dùng repository bao quanh thư mục hiện tại nếu tìm thấy; dùng `--root PATH` để chỉ định một checkout khác. Khi chạy ngoài repository, các lệnh đọc pattern mặc định dùng resource trong wheel.

## Console commands

```bash
viet-writing-lint article.md
viet-writing-lint article.md --format json
viet-writing-lint docs/ --recursive --root .
viet-writing-validate-skills --root .
viet-writing-validate-patterns --root .
viet-writing-validate-examples --root .
viet-writing-benchmark --root . --validate-only
viet-writing-generate-docs --root . --check
```

Các wrapper cũ vẫn hoạt động trong source checkout:

```bash
python scripts/lint_vietnamese.py article.md
python scripts/validate_skills.py
python scripts/validate_patterns.py
python scripts/validate_examples.py
python scripts/run_benchmarks.py --validate-only
python scripts/generate_pattern_docs.py --check
```

Linter trả exit code `1` khi có phát hiện cần review và `2` khi lệnh không thể chạy. Một phát hiện không chứng minh văn bản sai hay do AI viết.

## Taxonomy của linter

- `ERROR`: lỗi có thể chứng minh tương đối chắc, chẳng hạn từ bị lặp do gõ hoặc khoảng trắng sai.
- `WARNING`: cấu trúc có thể gây mơ hồ hoặc không nhất quán nhưng cần ngữ cảnh.
- `PREFERENCE`: lựa chọn phong cách, chỉ nên áp khi style đã được chọn.
- `HEURISTIC`: tín hiệu bề mặt như mật độ hoặc nhịp câu; reviewer phải đọc toàn phạm vi.

Mỗi pattern còn có `scope` và `aggregation`. Ví dụ, lặp mở đầu câu dùng `paragraph/sequence`, nhịp câu dùng `document/variance`, còn trộn đại từ dùng `document/consistency`.

## Corpus và benchmark

- 40 pattern có finding type, scope, aggregation, ngoại lệ và rủi ro false positive.
- 100 example có output mode, `context`, `must_preserve`, `must_not_add` và provenance review.
- 30 benchmark case có expected output mode, context, blocker cụ thể và ràng buộc bảo toàn.
- Kết quả review thủ công được kiểm bằng JSON Schema và có thể chứa nhiều reviewer cho một case.

Corpus hiện được coding agent audit theo từng cặp input + context → output. `agent-reviewed` không có nghĩa là đã được maintainer, người bản ngữ hoặc reviewer độc lập chấm. Repository chưa có baseline độc lập; benchmark hiện phục vụ thiết kế quy trình và regression dữ liệu, chưa phải bằng chứng về hiệu quả ngoài các case đã viết.

## Kiểm tra repository

```bash
ruff check .
pytest
python scripts/validate_skills.py
python scripts/validate_patterns.py
python scripts/validate_examples.py
python scripts/run_benchmarks.py --validate-only
python scripts/generate_pattern_docs.py --check
python -m build
```

Sinh lại tài liệu pattern sau khi sửa YAML:

```bash
python scripts/generate_pattern_docs.py
```

## Đóng góp

Đọc [CONTRIBUTING.md](CONTRIBUTING.md) và [hướng dẫn viết pattern](docs/pattern-authoring-guide.md). Example mới phải tự chứa đủ input/context, nêu phần phải giữ và phần cấm thêm, chọn output mode, rồi ghi đúng provenance review. Pattern mới cần taxonomy, phạm vi, cách aggregation, ngoại lệ, test và ví dụ không tự thêm dữ kiện.

## Giới hạn

Regex và validator cấu trúc không chứng minh semantic equivalence; chúng có thể bỏ sót hoặc báo nhầm. Một trăm example chưa đại diện đầy đủ cho khác biệt vùng miền, thế hệ, ngành nghề và register. Xem [limitations](docs/limitations.md) và [evaluation methodology](docs/evaluation-methodology.md).

## Attribution và license

Dự án tham khảo định dạng [Agent Skills](https://agentskills.io/specification), ý tưởng audit văn phong của [blader/humanizer](https://github.com/blader/humanizer) và kinh nghiệm bản địa hóa từ các dự án tiếng Trung, tiếng Hàn. Taxonomy và dữ liệu tiếng Việt trong repository được viết riêng. Chi tiết nằm trong [research notes](docs/research-notes.md).

Mã và nội dung gốc được phát hành theo [MIT License](LICENSE). Xem [ROADMAP.md](ROADMAP.md) cho kế hoạch tiếp theo.
