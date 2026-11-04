"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useRef, useState } from "react";
import { REPOSITORY_URL } from "../lib/repository";
import { Icon } from "./Icon";

const links = [
  { href: "/check", label: "Soát văn bản" },
  { href: "/examples", label: "Ví dụ thực tế" },
  { href: "/guide", label: "Hướng dẫn" },
  { href: "/start", label: "Dùng trong chatbot" },
];

export function SiteHeader({ stars }: { stars: number | null }) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const menuButton = useRef<HTMLButtonElement>(null);
  return (
    <header
      className="site-header"
      onKeyDown={(event) => {
        if (open && event.key === "Escape") {
          setOpen(false);
          menuButton.current?.focus();
        }
      }}
    >
      <div className="site-header-inner">
        <Link
          href="/"
          className="brand"
          onClick={() => setOpen(false)}
          aria-label="Vietnamese Writing Skills — Trang chủ"
        >
          <span className="brand-mark">
            <Icon name="pen" />
          </span>
          <span>Vietnamese Writing Skills</span>
        </Link>
        <button
          ref={menuButton}
          type="button"
          className="button-icon mobile-menu"
          aria-label={open ? "Đóng menu" : "Mở menu"}
          aria-expanded={open}
          aria-controls="primary-navigation"
          onClick={() => setOpen(!open)}
        >
          <Icon name={open ? "close" : "menu"} />
        </button>
        <nav
          id="primary-navigation"
          aria-label="Điều hướng chính"
          className={`site-nav ${open ? "is-open" : ""}`}
        >
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              aria-current={pathname === link.href ? "page" : undefined}
              onClick={() => setOpen(false)}
            >
              {link.label}
            </Link>
          ))}
          <a
            href={REPOSITORY_URL}
            className="repository-link"
            target="_blank"
            rel="noopener noreferrer"
            aria-label={
              stars === null
                ? "Xem mã nguồn trên GitHub"
                : `Xem mã nguồn trên GitHub, ${stars} sao`
            }
          >
            GitHub <Icon name="star" width="15" height="15" />
            {stars !== null && (
              <span className="star-count">
                {new Intl.NumberFormat("vi-VN", {
                  notation: "compact",
                  maximumFractionDigits: 1,
                }).format(stars)}
              </span>
            )}
          </a>
        </nav>
      </div>
    </header>
  );
}
