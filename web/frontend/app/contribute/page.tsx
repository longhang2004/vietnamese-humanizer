"use client";

import React, { useEffect, useState } from "react";
import { useCapabilities } from "../../components/CapabilityNav";
import { ContributeForm } from "../../components/ContributeForm";
import { Disclaimer } from "../../components/Disclaimer";
import { fetchSkills } from "../../lib/api";
import { SkillItem } from "../../lib/types";

export default function ContributePage() {
  const capabilities = useCapabilities();
  const [skills, setSkills] = useState<SkillItem[]>([]);

  useEffect(() => {
    if (!capabilities.contributions) return;

    async function loadSkills() {
      try {
        const skillsRes = await fetchSkills();
        setSkills(skillsRes.skills);
      } catch (err: unknown) {
        console.error("Failed to load skills:", err);
      }
    }
    loadSkills();
  }, [capabilities.contributions]);

  if (!capabilities.contributions) return null;

  return (
    <div>
      <Disclaimer />
      <ContributeForm skills={skills} />
    </div>
  );
}
