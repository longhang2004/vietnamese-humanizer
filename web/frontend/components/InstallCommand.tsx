"use client";

import { useState } from "react";
import { Icon } from "./Icon";

export function InstallCommand() {
  const command = "npx skills add longhang2004/vietnamese-humanizer";
  const [message, setMessage] = useState("");
  async function copy() {
    try { await navigator.clipboard.writeText(command); setMessage("Đã sao chép lệnh."); }
    catch { setMessage("Bạn có thể chọn và sao chép lệnh trực tiếp."); }
  }
  return <div className="install-block">
    <div className="install-command"><code>{command}</code><button type="button" className="button-icon" onClick={copy} aria-label="Sao chép lệnh cài skill"><Icon name={message.startsWith("Đã") ? "check" : "copy"} /></button></div>
    <p role="status" className="copy-status">{message}</p>
  </div>;
}
