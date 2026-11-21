import type { Metadata } from "next";
import { GettingStarted } from "../../components/GettingStarted";

export const metadata: Metadata = {
  title: "Dùng trong chatbot",
  description:
    "Chọn cách biên tập tiếng Việt trong ChatGPT, Claude, Gemini hoặc chatbot khác. Tải skill hoặc sao chép yêu cầu mẫu.",
  alternates: { canonical: "/start" },
};

export default function StartPage() {
  return <GettingStarted />;
}
