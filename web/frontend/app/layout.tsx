import { Analytics } from "@vercel/analytics/react";
import type { Metadata } from "next";
import Link from "next/link";
import React from "react";
import { CapabilityNav, CapabilityProvider } from "../components/CapabilityNav";
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
        alt: "Vietnamese Writing Skills banner",
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
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="min-h-[100dvh] flex flex-col bg-slate-50/60 text-slate-900 font-sans antialiased selection:bg-sky-100 selection:text-sky-900">
        <CapabilityProvider>
          {/* Frosted Glass Header */}
          <header className="sticky top-0 z-50 backdrop-blur-md bg-white/80 border-b border-slate-200/80 transition-all">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
              <Link href="/" className="flex items-center space-x-3 group">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-600 via-sky-500 to-emerald-500 flex items-center justify-center text-white shadow-sm shadow-sky-500/20 group-hover:scale-105 transition-transform">
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </div>
                <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-2">
                  <span className="font-extrabold text-slate-900 tracking-tight text-base sm:text-lg group-hover:text-sky-600 transition-colors">
                    Vietnamese Writing Skills
                  </span>
                </div>
              </Link>

              <CapabilityNav />
            </div>
          </header>

          {/* Main Content Area */}
          <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {children}
          </main>

          {/* Footer */}
          <footer className="bg-white border-t border-slate-200/80 py-8 mt-16 text-center text-xs text-slate-500">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
              <p className="text-slate-400 max-w-2xl text-center md:text-right">
                Công cụ nhận diện tín hiệu văn phong cho người viết và biên tập viên. Không chấm điểm xác suất AI, không suy đoán tác giả.
              </p>
            </div>
          </footer>
        </CapabilityProvider>
        <Analytics />
      </body>
    </html>
  );
}
