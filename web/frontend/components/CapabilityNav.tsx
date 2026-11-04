"use client";

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
