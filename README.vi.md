[English](README.md) | **Tiếng Việt**

# Vietnamese Writing Skills

[![Live Web App](https://img.shields.io/badge/Web_App-Trải_nghiệm_ngay-brightgreen?style=flat&logo=vercel)](https://vietnamese-humanizer-g1o9.vercel.app/)
[![CI](https://github.com/longhang2004/vietnamese-humanizer/actions/workflows/ci.yml/badge.svg)](https://github.com/longhang2004/vietnamese-humanizer/actions/workflows/ci.yml)
[![Python 3.11–3.14](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

🌐 **Phiên bản web**: [https://vietnamese-humanizer-g1o9.vercel.app/](https://vietnamese-humanizer-g1o9.vercel.app/)

Bộ công cụ này biên tập tiếng Việt mà không làm thay đổi dữ kiện. Mục tiêu là giúp văn bản đầu vào rõ hơn, tự nhiên hơn và hợp với ngữ cảnh.

Repository mang tên `vietnamese-humanizer` vì đó là URL của dự án. Sản phẩm có tên **Vietnamese Writing Skills** vì gồm bốn skill, không chỉ có humanizer. Gói phân phối Python là `vietnamese-writing-skills`; package import là `vietnamese_writing_skills`.

Dự án không phân loại tác giả, không tạo "AI probability score" và không hướng dẫn vượt detector. Linter chỉ nêu các tín hiệu bề mặt để người đọc đánh giá.

## Bốn skill

| Skill | Dùng khi | Không dùng khi |
| --- | --- | --- |
| `humanizer-vi` | Văn bản có vẻ theo khuôn, sáo, đều nhịp hoặc lệch giọng | Suy đoán tác giả, lách detector, hoặc chỉ soát lỗi máy móc |
| `translationese-cleaner-vi` | Câu tiếng Việt bám quá sát trật tự, ẩn dụ hoặc lối danh hóa tiếng Anh | Tự thay thuật ngữ chuẩn hoặc làm yếu văn bản pháp lý |
| `grammar-checker-vi` | Kiểm tra chính tả, dấu câu, cấu trúc và chỗ mơ hồ | Ép một phong cách hoặc sửa code, URL, identifier |
| `style-guide-vi` | Giữ cách xưng hô, thuật ngữ, số và định dạng nhất quán | Ghi đè style guide riêng hoặc thay đổi dữ kiện |

## Ví dụ bảo toàn dữ kiện

Trước:

> Trong bài viết này, chúng ta sẽ cùng tìm hiểu cách Redis lưu dữ liệu thường dùng trong bộ nhớ để giảm số lần truy cập nguồn dữ liệu chậm hơn.

Sau:

> Redis lưu dữ liệu thường dùng trong bộ nhớ, nhờ đó hệ thống ít phải truy cập nguồn dữ liệu chậm hơn.

Bản viết lại chỉ bỏ phần thông báo. Cơ chế Redis đã có trong văn bản đầu vào, nên không được thay bằng câu chung như "Redis giúp tối ưu hiệu suất". Trong corpus, mọi thông tin ngoài văn bản đầu vào phải ghi rõ ở trường `context`.

## Bốn output mode

- `clean_rewrite`: Bản viết lại giữ nguyên ý và có thể thay trực tiếp cho input.
- `review_comment`: Nhận xét cho người viết khi thiếu nguồn hoặc bằng chứng, không phải replacement text.
- `needs_author_decision`: Văn bản đầu vào có nhiều cách hiểu, nên cần người viết quyết định trước khi sửa.
- `no_change`: Input đã phù hợp. Không sửa chỉ để tạo ra khác biệt.

Agent không cần viết lại mọi input. Khi chủ thể, phạm vi, ngày tháng hoặc mức độ nghĩa vụ còn mơ hồ, không đoán là cách xử lý đúng.

## Cài Agent Skills từ repository

```bash
git clone https://github.com/longhang2004/vietnamese-humanizer.git
cd vietnamese-humanizer
```

Trỏ agent tương thích với Agent Skills tới thư mục cần dùng trong `skills/`, hoặc sao chép thư mục đó vào nơi agent đọc skill. Mỗi skill có `SKILL.md`, tài liệu tham chiếu và tài sản cần thiết.

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

Wheel gồm pattern, schema, skill Markdown, example và benchmark resources. Nếu tìm thấy repository bao quanh thư mục hiện tại, CLI sẽ dùng repository đó. Dùng `--root PATH` để chọn checkout khác. Khi chạy ngoài repository, các lệnh đọc pattern dùng resource trong wheel.

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

Source checkout vẫn dùng được các wrapper cũ:

```bash
python scripts/lint_vietnamese.py article.md
python scripts/validate_skills.py
python scripts/validate_patterns.py
python scripts/validate_examples.py
python scripts/run_benchmarks.py --validate-only
python scripts/generate_pattern_docs.py --check
```

Linter trả exit code `1` khi có phát hiện cần đánh giá và `2` khi lệnh không chạy được. Một phát hiện không chứng minh văn bản sai hoặc do AI viết.

## Taxonomy của linter

- `ERROR`: lỗi có thể chứng minh tương đối chắc, chẳng hạn từ bị lặp do gõ hoặc khoảng trắng sai.
- `WARNING`: cấu trúc có thể gây mơ hồ hoặc không nhất quán nhưng cần ngữ cảnh.
- `PREFERENCE`: lựa chọn phong cách, chỉ nên áp khi style đã được chọn.
- `HEURISTIC`: tín hiệu bề mặt như mật độ hoặc nhịp câu; reviewer phải đọc toàn phạm vi.

Mỗi pattern cũng có `scope` và `aggregation`. Lặp mở đầu câu dùng `paragraph/sequence`; nhịp câu dùng `document/variance`; trộn đại từ dùng `document/consistency`.

## Corpus và benchmark

Catalog có 40 pattern, mỗi pattern nêu finding type, scope, aggregation, ngoại lệ và rủi ro false positive. Có 100 example với output mode, `context`, `must_preserve`, `must_not_add` và nguồn gốc đánh giá. Có 30 benchmark case ghi expected output mode, context, blocker cụ thể và ràng buộc bảo toàn. JSON Schema kiểm tra kết quả đánh giá thủ công; một case có thể có nhiều reviewer.

Coding agent đã audit từng cặp input + context → output trong corpus. `agent-reviewed` không có nghĩa maintainer, người bản ngữ hoặc reviewer độc lập đã đánh giá. Repository chưa có baseline độc lập. Benchmark hiện hỗ trợ thiết kế quy trình và regression dữ liệu, chưa chứng minh hiệu quả ngoài các case đã viết.

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

Đọc [CONTRIBUTING.vi.md](CONTRIBUTING.vi.md), [mục lục tài liệu](docs/README.md) và [hướng dẫn viết pattern](docs/pattern-authoring-guide.md). Example mới phải có đủ input và context để kiểm chứng, nêu phần phải giữ cùng phần cấm thêm, chọn output mode và ghi đúng nguồn gốc đánh giá. Pattern mới cần taxonomy, phạm vi, cách aggregation, ngoại lệ, test và ví dụ không tự thêm dữ kiện.

## Giới hạn

Regex và validator cấu trúc không thể chứng minh semantic equivalence. Chúng có thể bỏ sót vấn đề hoặc báo nhầm. Một trăm example chưa đại diện đầy đủ cho mọi khác biệt về vùng miền, thế hệ, ngành nghề và register. Xem [limitations](docs/limitations.md) và [evaluation methodology](docs/evaluation-methodology.md).

## Ủng hộ dự án

Nếu Vietnamese Writing Skills hữu ích, bạn có thể ủng hộ việc duy trì dự án. Trước khi xác nhận chuyển khoản, hãy kiểm tra người nhận là **HANG NHUT LONG** tại **BIDV**.

<p align="center">
  <a href="assets/donate-vietqr.png">
    <img src="https://raw.githubusercontent.com/longhang2004/vietnamese-humanizer/main/assets/donate-vietqr.png" alt="Mã VietQR ủng hộ HANG NHUT LONG tại BIDV" width="360">
  </a>
</p>

## Đóng góp & Cảm ơn

- **Hàng Nhựt Long** ([@longhang2004](https://github.com/longhang2004)) — Duyệt & phát triển chính.
- **Lê Ngọc Phương Thư** (`lengocphuongthuct2006@gmail.com`) — Đề xuất và lên ý tưởng xây dựng phiên bản Web Application.

Dự án tham khảo định dạng [Agent Skills](https://agentskills.io/specification), các ý tưởng audit văn phong của [blader/humanizer](https://github.com/blader/humanizer) và kinh nghiệm bản địa hóa từ dự án tiếng Trung, tiếng Hàn. Taxonomy cùng dữ liệu tiếng Việt trong repository được viết độc lập. Xem thêm [research notes](docs/research-notes.md).

Mã và nội dung gốc được phát hành theo [MIT License](LICENSE). Xem [ROADMAP.md](ROADMAP.md) cho kế hoạch tiếp theo.
