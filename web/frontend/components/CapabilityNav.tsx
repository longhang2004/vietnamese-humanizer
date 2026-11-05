"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { fetchHealth } from "../lib/api";
import type { HealthResponse } from "../lib/types";

type Capabilities = HealthResponse["capabilities"];
type CapabilityState = Capabilities & {
  status: "loading" | "ready" | "unavailable";
};

const disabledCapabilities: Capabilities = {
  rewrite: false,
  contributions: false,
};
const CapabilityContext = createContext<CapabilityState>({
  ...disabledCapabilities,
  status: "unavailable",
});

export function CapabilityProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [capabilities, setCapabilities] = useState<CapabilityState>({
    ...disabledCapabilities,
    status: "loading",
  });
  useEffect(() => {
    let active = true;
    fetchHealth()
      .then((health) => {
        if (!active) return;
        setCapabilities({
          rewrite: health.capabilities.rewrite === true,
          contributions: health.capabilities.contributions === true,
          status: "ready",
        });
      })
      .catch(() => {
        if (active)
          setCapabilities({ ...disabledCapabilities, status: "unavailable" });
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

export function useCapabilities(): CapabilityState {
  return useContext(CapabilityContext);
}
