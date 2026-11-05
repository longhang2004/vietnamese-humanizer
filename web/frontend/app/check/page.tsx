import type { Metadata } from "next";
import { CapabilityProvider } from "../../components/CapabilityNav";
import { Checker } from "../../components/Checker";

export const metadata: Metadata = {
  title: "Soát văn phong tiếng Việt",
  description:
    "Kiểm tra ngữ pháp, văn phong, câu dịch chưa tự nhiên và lối viết theo khuôn trong văn bản tiếng Việt. Đọc lý do và cân nhắc từng gợi ý theo ngữ cảnh.",
  alternates: { canonical: "/check" },
};

export default function CheckPage() {
  return (
    <CapabilityProvider>
      <Checker />
    </CapabilityProvider>
  );
}
