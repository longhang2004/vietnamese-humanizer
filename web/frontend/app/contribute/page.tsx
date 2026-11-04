"use client";

import React, { useEffect, useState } from "react";
import { CapabilityProvider, useCapabilities } from "../../components/CapabilityNav";
import { ContributeForm } from "../../components/ContributeForm";
import { fetchSkills } from "../../lib/api";
import { SkillItem } from "../../lib/types";

function ContributionContent() {
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

  if (!capabilities.contributions) return <section className="page-heading"><h1>Góp mẫu văn bản</h1><p>Phần gửi mẫu hiện chưa mở. Bạn có thể góp ý hoặc báo trường hợp cần xem lại trong <a className="text-link" href="https://github.com/longhang2004/vietnamese-humanizer/issues">issue trên GitHub</a>.</p></section>;

  return (
    <div className="py-12">
      <ContributeForm skills={skills} />
    </div>
  );
}

export default function ContributePage() {
  return <CapabilityProvider><ContributionContent /></CapabilityProvider>;
}
