import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Góp mẫu văn bản",
  alternates: { canonical: "/contribute" },
};

export default function ContributionLayout({
  children,
}: {
  children: ReactNode;
}) {
  return children;
}
