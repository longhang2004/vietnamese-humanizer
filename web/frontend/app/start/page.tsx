import type { Metadata } from "next";
import { GettingStarted } from "../../components/GettingStarted";

export const metadata: Metadata = {
  title: "Bắt đầu sử dụng",
  description: "Chọn chatbot và việc cần làm, rồi tải skill hoặc sao chép yêu cầu mẫu để biên tập tiếng Việt. Có hướng dẫn cho ChatGPT, Claude và Gemini.",
  alternates: { canonical: "/start" },
};

export default function StartPage() {
  return <GettingStarted />;
}
