export const REPOSITORY_URL =
  "https://github.com/longhang2004/vietnamese-humanizer";

export async function getRepositoryStars(): Promise<number | null> {
  try {
    const response = await fetch(
      "https://api.github.com/repos/longhang2004/vietnamese-humanizer",
      {
        headers: { Accept: "application/vnd.github+json" },
        next: { revalidate: 3600 },
        signal: AbortSignal.timeout(2500),
      },
    );
    if (!response.ok) return null;
    const data = await response.json();
    const count: unknown = data.stargazers_count;
    return typeof count === "number" &&
      Number.isSafeInteger(count) &&
      count >= 0
      ? count
      : null;
  } catch {
    return null;
  }
}
