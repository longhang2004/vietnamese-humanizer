import { expect, test } from "vitest";
import { computeWordDiff } from "./diff";

test("returns identical or empty segments for unchanged inputs", () => {
  expect(computeWordDiff("", "")).toEqual([]);
  expect(computeWordDiff("Câu giữ nguyên.", "Câu giữ nguyên.")).toEqual([
    { kind: "equal", text: "Câu giữ nguyên." },
  ]);
});

test("tracks word additions, deletions and replacements in Vietnamese text", () => {
  const original = "Nhóm thực hiện việc kiểm tra báo cáo lúc 15:00.";
  const revised = "Nhóm trực tiếp kiểm tra báo cáo trước 15:00.";
  const segments = computeWordDiff(original, revised);

  expect(
    segments.some(
      (item) => item.kind === "removed" && item.text.includes("thực hiện việc"),
    ),
  ).toBe(true);
  expect(
    segments.some(
      (item) => item.kind === "added" && item.text.includes("trực tiếp"),
    ),
  ).toBe(true);
  expect(
    segments.some(
      (item) => item.kind === "removed" && item.text.includes("lúc"),
    ),
  ).toBe(true);
  expect(
    segments.some(
      (item) => item.kind === "added" && item.text.includes("trước"),
    ),
  ).toBe(true);

  const reconstructedOriginal = segments
    .filter((item) => item.kind !== "added")
    .map((item) => item.text)
    .join("");
  const reconstructedRevised = segments
    .filter((item) => item.kind !== "removed")
    .map((item) => item.text)
    .join("");
  expect(reconstructedOriginal).toBe(original);
  expect(reconstructedRevised).toBe(revised);
});

test("handles full additions, full removals and line breaks", () => {
  expect(computeWordDiff("", "Đoạn mới")).toEqual([
    { kind: "added", text: "Đoạn mới" },
  ]);
  expect(computeWordDiff("Đoạn cũ", "")).toEqual([
    { kind: "removed", text: "Đoạn cũ" },
  ]);

  const segments = computeWordDiff("Dòng 1.\nDòng 2.", "Dòng 1.\n\nDòng 2.");
  expect(
    segments
      .filter((item) => item.kind !== "removed")
      .map((item) => item.text)
      .join(""),
  ).toBe("Dòng 1.\n\nDòng 2.");
});
