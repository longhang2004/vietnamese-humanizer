"use client";

import React, { useEffect, useState } from "react";
import {
  CapabilityProvider,
  useCapabilities,
} from "../../components/CapabilityNav";
import { ContributeForm } from "../../components/ContributeForm";
import { fetchSkills } from "../../lib/api";
import type { SkillItem } from "../../lib/types";
import styles from "../../components/workspace.module.css";

function ContributionContent() {
  const capabilities = useCapabilities();
  const [skills, setSkills] = useState<SkillItem[]>([]);
  useEffect(() => {
    if (!capabilities.contributions) return;
    let active = true;
    fetchSkills()
      .then((response) => {
        if (active) setSkills(response.skills);
      })
      .catch(() => {
        /* The form retains its built-in skill choices. */
      });
    return () => {
      active = false;
    };
  }, [capabilities.contributions]);
  return (
    <div className={styles.page}>
      <header className={styles.heading}>
        <div>
          <h1>Góp mẫu văn bản</h1>
          <p>
            Gửi đoạn gốc và cách sửa bạn đề xuất. Nhóm duy trì sẽ xem xét trước
            khi thêm ví dụ vào bộ dữ liệu của dự án.
          </p>
        </div>
      </header>
      {capabilities.status === "loading" ? (
        <div className={styles.loadingRoute}>
          <p role="status">Đang kiểm tra khả năng gửi mẫu…</p>
          <div aria-hidden="true" className={styles.skeleton}>
            <div className={styles.skeletonLine} />
            <div className={styles.skeletonLine} />
          </div>
        </div>
      ) : capabilities.contributions ? (
        <ContributeForm skills={skills} />
      ) : (
        <p className={styles.notice}>
          Phần gửi mẫu hiện chưa mở. Bạn có thể góp ý hoặc báo trường hợp cần
          xem lại trong{" "}
          <a
            className="text-link"
            href="https://github.com/longhang2004/vietnamese-humanizer/issues"
          >
            issue trên GitHub
          </a>
          .
        </p>
      )}
    </div>
  );
}
export default function ContributePage() {
  return (
    <CapabilityProvider>
      <ContributionContent />
    </CapabilityProvider>
  );
}
