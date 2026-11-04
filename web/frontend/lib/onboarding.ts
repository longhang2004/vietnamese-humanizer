import downloads from "../public/downloads/manifest.json";

export const starterSkills = downloads.skills;
export const docsCheckedOn = downloads.docs_checked_on.split("-").reverse().join("/");
export const chatgptInstallUrl: string | null = downloads.chatgpt_install_url;

export type StarterSkill = (typeof starterSkills)[number];
export type Platform = "chatgpt" | "claude" | "gemini" | "other";

export function starterPrompt(skill: StarterSkill): string {
  return `${downloads.quick_start}\n\n${skill.request}\n\nVăn bản cần biên tập:\n[Dán văn bản của bạn vào đây]`;
}

export function skillDownload(platform: "claude" | "gemini", skill: StarterSkill) {
  const filename = `${platform}/${skill.id}.zip`;
  const artifact = (downloads.artifacts as Record<string, { bytes: number }>)[filename];
  return {
    href: `/downloads/${filename}`,
    size: `${Math.ceil(artifact.bytes / 1024)} KB`,
  };
}
