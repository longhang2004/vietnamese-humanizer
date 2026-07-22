**Tiếng Việt** | [English](SECURITY.md)

# Chính sách bảo mật (Security Policy)

## Các phiên bản được hỗ trợ

Các bản sửa lỗi bảo mật nhắm đến bản phát hành mới nhất và nhánh `main`. Dự án không bảo đảm backport cho các bản cũ. Hãy xem `pyproject.toml` và `CHANGELOG.md` để biết phiên bản hiện tại, thay vì dựa vào ví dụ phiên bản trong tài liệu kế hoạch lịch sử.

## Báo cáo lỗ hổng bảo mật bí mật

Nếu GitHub hiển thị [biểu mẫu báo cáo riêng của repository](https://github.com/longhang2004/vietnamese-humanizer/security/advisories/new), hãy dùng biểu mẫu đó cho lỗ hổng nghi ngờ. Liên kết này không khẳng định một cài đặt GitHub cụ thể đang bật. Nếu không có biểu mẫu, hãy mở một [issue tối giản](https://github.com/longhang2004/vietnamese-humanizer/issues/new/choose) để nhờ `@longhang2004` trao đổi riêng; không ghi chi tiết khai thác hay dữ liệu nhạy cảm trong issue công khai.

Báo cáo cần kèm theo phiên bản hoặc commit bị ảnh hưởng, ví dụ mẫu nhỏ có thể tái hiện lỗi, tác động dự kiến và gợi ý khắc phục. Xóa bỏ thông tin xác thực, thông tin cá nhân hoặc dữ liệu riêng tư khỏi báo cáo.

Dự án này xử lý các đoạn văn bản mẫu. Vui lòng **không** gửi văn bản nhạy cảm của người dùng, tài liệu bảo mật hoặc dữ liệu sản xuất thực tế. Thay vào đó, hãy dùng văn bản giả lập ngắn gọn nhưng vẫn giữ được hành vi cần kiểm tra.

Các báo cáo dương tính giả (false-positive), góp ý chất lượng ngôn ngữ hoặc thắc mắc về cách biên tập không được coi là lỗ hổng bảo mật. Vui lòng lọc bỏ dữ liệu nhạy cảm trước khi dùng mẫu issue chuẩn của repository.

## Ranh giới dữ liệu của web app

- Yêu cầu lint deterministic gửi văn bản tới backend đã cấu hình để nhận danh sách phát hiện. Mã nguồn dự án không lưu input lint thành contribution.
- Tính năng viết lại mặc định tắt. Khi operator bật tính năng và cung cấp `GEMINI_API_KEY`, văn bản cần viết lại được gửi tới tích hợp Gemini đã cấu hình. Hãy xem điều khoản hiện hành của nhà cung cấp trước khi bật; dự án không khẳng định cách nhà cung cấp lưu giữ hay dùng dữ liệu huấn luyện.
- Tính năng nhận đóng góp mặc định tắt. Khi bật, contribution được lưu vào cơ sở dữ liệu đã cấu hình để maintainer xem xét. Contribution không tự động trở thành corpus hay dữ liệu huấn luyện; muốn thêm vào `examples/` hoặc `benchmarks/` vẫn phải qua pull request và quy trình review thủ công.
- Vercel Analytics vẫn được cài và render trong frontend Wave 1. Mã nguồn dự án không gửi custom analytics event, user ID, văn bản document/lint/rewrite/contribution hay thuộc tính suy ra từ văn bản. Phát biểu này chỉ nói về mã nguồn dự án, không khẳng định thời gian lưu giữ của nhà cung cấp, log hosting, mã hóa, APM hay cấu hình deploy.
