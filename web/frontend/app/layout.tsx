import type { Metadata } from "next";
import Link from "next/link";
import React from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: "Vietnamese Writing Skills - Công cụ Rà soát Văn phong Tiếng Việt",
  description: "Trang web rà soát và gợi ý gọt giũa văn phong tiếng Việt cho người viết và biên tập viên",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi">
      <body className="min-h-screen flex flex-col">
        <header className="bg-white border-b border-gray-200 sticky top-0 z-40 shadow-sm">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <Link href="/" className="flex items-center space-x-2">
              <span className="text-xl">✍️</span>
              <span className="font-bold text-gray-900 text-base sm:text-lg">
                Vietnamese Writing Skills
              </span>
              <span className="text-xs bg-brand-100 text-brand-800 px-2 py-0.5 rounded font-mono font-semibold">
                v0.2.0
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
              Vietnamese Writing Skills — Bộ công cụ Agent Skills và linter văn phong tiếng Việt.
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
