# Ghi chú triển khai

API có thể trả lỗi 429 nếu client gửi quá 100 yêu cầu mỗi phút. Khi gặp lỗi này, client tạm dừng các lần thử song song, chờ theo trường `Retry-After` rồi chỉ gửi lại yêu cầu sau khoảng thời gian máy chủ chỉ định. Hệ thống không bảo đảm yêu cầu tiếp theo sẽ thành công.

Nhóm vận hành theo dõi tỷ lệ lỗi trong 30 phút sau mỗi lần phát hành. Nếu tỷ lệ vượt 2%, người trực ca có thể quay về bản trước.
