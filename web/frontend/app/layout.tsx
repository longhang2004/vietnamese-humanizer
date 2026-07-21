import type { Metadata } from "next";
import Link from "next/link";
import React from "react";
import "./globals.css";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://vietnamese-humanizer-g1o9.vercel.app";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "Vietnamese Writing Skills - Rà soát & Gọt giũa Văn phong Tiếng Việt",
    template: "%s | Vietnamese Writing Skills",
  },
  description:
    "Công cụ rà soát và gợi ý gọt giũa văn phong tiếng Việt cho người viết và biên tập viên. Nêu tín hiệu sáo rỗng, gọt dịch thuật ngữ và gợi ý viết lại tự nhiên.",
  keywords: [
    "rà soát văn phong tiếng việt",
    "gọt giũa văn phong",
    "humanizer tiếng việt",
    "kiểm tra văn phong",
    "linter tiếng việt",
    "gọt dịch thuật ngữ",
    "quy chuẩn báo chí",
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
    title: "Vietnamese Writing Skills - Công cụ Rà soát & Gọt giũa Văn phong Tiếng Việt",
    description:
      "Công cụ trực tuyến hỗ trợ người viết và biên tập viên rà soát lỗi sáo rỗng, gọt dịch thuật ngữ và viết lại tiếng Việt tự nhiên bằng AI.",
    url: siteUrl,
    siteName: "Vietnamese Writing Skills",
    locale: "vi_VN",
    type: "website",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 675,
        alt: "Vietnamese Writing Skills v0.3.0 Banner",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Vietnamese Writing Skills - Công cụ Rà soát & Gọt giũa Văn phong Tiếng Việt",
    description:
      "Công cụ trực tuyến hỗ trợ người viết và biên tập viên rà soát lỗi sáo rỗng, gọt dịch thuật ngữ và viết lại tiếng Việt tự nhiên bằng AI.",
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
  alternateName: "Vietnamese Humanizer & Linter",
  url: siteUrl,
  applicationCategory: "BusinessApplication",
  operatingSystem: "All",
  offers: {
    "@type": "Offer",
    price: "0",
    priceCurrency: "VND",
  },
  description:
    "Công cụ rà soát và gợi ý gọt giũa văn phong tiếng Việt cho người viết và biên tập viên dựa trên bộ Agent Skills.",
  inLanguage: "vi-VN",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="min-h-screen flex flex-col">
        <header className="bg-white border-b border-gray-200 sticky top-0 z-40 shadow-sm">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <Link href="/" className="flex items-center space-x-2">
              <span className="text-xl">✍️</span>
              <span className="font-bold text-gray-900 text-base sm:text-lg">
                Vietnamese Writing Skills
              </span>
              <span className="text-xs bg-brand-100 text-brand-800 px-2 py-0.5 rounded font-mono font-semibold">
                v0.3.0
              </span>
            </Link>

            <nav className="flex items-center space-x-4 text-xs sm:text-sm font-medium">
              <Link href="/" className="text-gray-700 hover:text-brand-600 transition-colors">
                Rà soát văn phong
              </Link>
              <Link
                href="/contribute"
                className="px-3 py-1.5 bg-brand-50 text-brand-700 hover:bg-brand-100 rounded-md border border-brand-200 transition-colors"
              >
                + Đóng góp case
              </Link>
            </nav>
          </div>
        </header>

        <main className="flex-grow max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {children}
        </main>

        <footer className="bg-white border-t border-gray-200 py-6 mt-12 text-center text-xs text-gray-500">
          <div className="max-w-6xl mx-auto px-4">
            <p>
              Vietnamese Writing Skills — Bộ công cụ Agent Skills và linter văn phong tiếng Việt (v0.3.0).
            </p>
            <p className="mt-1 text-gray-400">
              Công cụ nêu tín hiệu hỗ trợ người viết review. Không phải AI-detector, không chấm điểm xác suất tác giả.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
