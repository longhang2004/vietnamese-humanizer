import downloads from "../public/downloads/manifest.json";

export const starterSkills = downloads.skills;
export const docsCheckedOn = downloads.docs_checked_on
  .split("-")
  .reverse()
  .join("/");
export const chatgptInstallUrl: string | null = downloads.chatgpt_install_url;

export type StarterSkill = (typeof starterSkills)[number];
export type Platform = "chatgpt" | "claude" | "gemini" | "other";

export const starterScenarios = [
  {
    id: "default",
    label: "Mặc định theo việc đã chọn",
    note: "",
  },
  {
    id: "spoken_script",
    label: "Kịch bản nói / Vlog / Video kiến thức",
    note: "Ngữ cảnh: Kịch bản nói để đọc thành tiếng hoặc dẫn video; giữ lượt thoại tự nhiên, câu ngắn, tránh cụm báo hiệu bài viết.",
  },
  {
    id: "banter_social",
    label: "Bài đăng mạng xã hội cợt nhả / Dí dỏm",
    note: "Ngữ cảnh: Bài đăng mạng xã hội giọng cợt nhả, dí dỏm; giữ nhịp câu đùa và dừng đúng điểm rơi, không giải thích lại.",
  },
  {
    id: "satire",
    label: "Văn trào phúng / Châm biếm",
    note: "Ngữ cảnh: Văn trào phúng, châm biếm; giữ nghịch ngữ, khen ngược và phép nhại văn phong, không giảng đạo lý.",
  },
] as const;

export type StarterScenarioId = (typeof starterScenarios)[number]["id"];

export function starterPrompt(
  skill: StarterSkill,
  scenarioId: StarterScenarioId = "default",
): string {
  const scenario = starterScenarios.find((item) => item.id === scenarioId);
  const scenarioBlock = scenario?.note ? `\n\n${scenario.note}` : "";
  return `${downloads.quick_start}\n\n${skill.request}${scenarioBlock}\n\nĐoạn mẫu giọng viết của tôi (tùy chọn — bỏ qua nếu không dùng; chỉ học nhịp và xưng hô, không lấy dữ kiện):\n[Dán 1–2 đoạn bạn từng viết, hoặc xóa mục này]\n\nVăn bản cần biên tập:\n[Dán văn bản của bạn vào đây]`;
}

export function skillDownload(
  platform: "claude" | "gemini",
  skill: StarterSkill,
) {
  const filename = `${platform}/${skill.id}.zip`;
  const artifact = (downloads.artifacts as Record<string, { bytes: number }>)[
    filename
  ];
  return {
    href: `/downloads/${filename}`,
    size: `${Math.ceil(artifact.bytes / 1024)} KB`,
  };
}
