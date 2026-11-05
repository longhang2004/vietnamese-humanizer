import { Analytics } from "@vercel/analytics/react";
import type { Metadata } from "next";
import React from "react";
import { SiteHeader } from "../components/SiteHeader";
import { SiteFooter } from "../components/SiteFooter";
import { getRepositoryStars } from "../lib/repository";
import "./globals.css";

const siteUrl =
  process.env.NEXT_PUBLIC_SITE_URL ||
  "https://vietnamese-humanizer-g1o9.vercel.app";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "Vietnamese Writing Skills — Soát văn phong tiếng Việt",
    template: "%s | Vietnamese Writing Skills",
  },
  description:
    "Soát lỗi tiếng Việt, xem lại câu sáo rỗng hoặc dịch chưa tự nhiên và giữ cách viết nhất quán. Dùng trên web hoặc tải skill cho chatbot của bạn.",
  keywords: [
    "rà soát văn phong tiếng việt",
    "gọt giũa văn phong",
    "humanizer tiếng việt",
    "kiểm tra văn phong",
    "linter tiếng việt",
    "sửa câu dịch chưa tự nhiên",
    "cách viết nhất quán",
    "agent skills tiếng việt",
  ],
  authors: [{ name: "Vietnamese Writing Skills Team" }],
  creator: "Vietnamese Writing Skills",
  publisher: "Vietnamese Writing Skills",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "Vietnamese Writing Skills — Soát văn phong tiếng Việt",
    description:
      "Soát lỗi tiếng Việt, xem lại câu sáo rỗng hoặc dịch chưa tự nhiên và giữ cách viết nhất quán. Dùng trên web hoặc tải skill cho chatbot của bạn.",
    url: siteUrl,
    siteName: "Vietnamese Writing Skills",
    locale: "vi_VN",
    type: "website",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 675,
        alt: "Vietnamese Writing Skills — công cụ soát văn phong tiếng Việt",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Vietnamese Writing Skills — Soát văn phong tiếng Việt",
    description:
      "Soát lỗi tiếng Việt, xem lại câu sáo rỗng hoặc dịch chưa tự nhiên và giữ cách viết nhất quán. Dùng trên web hoặc tải skill cho chatbot của bạn.",
    images: ["/og-image.jpg"],
  },
  icons: {
    icon: "/favicon.png",
    shortcut: "/favicon.png",
    apple: "/apple-icon.png",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "WebApplication",
  name: "Vietnamese Writing Skills",
  url: siteUrl,
  applicationCategory: "BusinessApplication",
  operatingSystem: "All",
  offers: {
    "@type": "Offer",
    price: "0",
    priceCurrency: "VND",
  },
  description:
    "Công cụ soát văn phong tiếng Việt, giúp người viết nhận ra chỗ cần xem lại và cân nhắc cách sửa theo ngữ cảnh.",
  inLanguage: "vi-VN",
};

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const stars = await getRepositoryStars();
  return (
    <html lang="vi">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="site-shell antialiased">
        <a className="skip-link" href="#main-content">
          Đến nội dung chính
        </a>
        <SiteHeader stars={stars} />
        <main id="main-content" className="site-main">
          {children}
        </main>
        <SiteFooter />
        <Analytics />
      </body>
    </html>
  );
}
