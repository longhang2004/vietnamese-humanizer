import type { Metadata } from "next";
import { ABReview } from "../../components/ABReview";

export const metadata: Metadata = {
  title: "Chấm A/B",
  description:
    "Đọc hai bản biên tập được giấu nhãn và góp lựa chọn để cải thiện bộ skill tiếng Việt.",
  alternates: { canonical: "/review" },
};

export default function ReviewPage() {
  return <ABReview />;
}
