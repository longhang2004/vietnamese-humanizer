"use client";

import Link from "next/link";
import React, { createContext, useContext, useEffect, useState } from "react";
import { fetchHealth } from "../lib/api";
import { HealthResponse } from "../lib/types";

type Capabilities = HealthResponse["capabilities"];

const disabledCapabilities: Capabilities = {
  rewrite: false,
  contributions: false,
};

const CapabilityContext = createContext<Capabilities>(disabledCapabilities);

export function CapabilityProvider({ children }: { children: React.ReactNode }) {
  const [capabilities, setCapabilities] = useState<Capabilities>(disabledCapabilities);

  useEffect(() => {
    let active = true;

    fetchHealth()
      .then((health) => {
        if (!active) return;

        setCapabilities({
          rewrite: health.capabilities.rewrite === true,
          contributions: health.capabilities.contributions === true,
        });
      })
      .catch(() => {
        // Optional features remain disabled when health is unavailable.
      });

    return () => {
      active = false;
    };
  }, []);

  return (
    <CapabilityContext.Provider value={capabilities}>
      {children}
    </CapabilityContext.Provider>
  );
}

export function useCapabilities(): Capabilities {
  return useContext(CapabilityContext);
}

export function CapabilityNav() {
  const capabilities = useCapabilities();

  return (
    <nav
      className="flex items-center space-x-3 text-xs sm:text-sm font-medium"
      aria-label="Điều hướng chính"
    >
      <Link
        href="/"
        className="px-3 py-1.5 rounded-lg text-slate-600 hover:text-sky-600 hover:bg-slate-100/80 transition-all"
      >
        Soát văn phong
      </Link>
      {capabilities.contributions && (
        <Link
          href="/contribute"
          className="px-3.5 py-1.5 bg-sky-600 hover:bg-sky-700 text-white rounded-lg font-semibold shadow-sm shadow-sky-600/20 active:scale-[0.98] transition-all flex items-center space-x-1.5"
        >
          <svg
            className="w-4 h-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2.5}
            aria-hidden="true"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          <span>Góp mẫu văn bản</span>
        </Link>
      )}
    </nav>
  );
}
