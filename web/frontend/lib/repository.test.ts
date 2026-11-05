import { afterEach, expect, test, vi } from "vitest";
import { getRepositoryStars } from "./repository";

afterEach(() => vi.unstubAllGlobals());

test("reads the actual star count, including zero", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ stargazers_count: 0 }),
    }),
  );
  expect(await getRepositoryStars()).toBe(0);
});

test.each([
  { ok: false, json: async () => ({ message: "rate limited" }) },
  { ok: true, json: async () => ({ stargazers_count: -1 }) },
  { ok: true, json: async () => ({ stargazers_count: "42" }) },
])("keeps an unavailable count distinct from zero", async (response) => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response));
  expect(await getRepositoryStars()).toBeNull();
});

test("keeps the repository link usable when the network fails", async () => {
  vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
  expect(await getRepositoryStars()).toBeNull();
});
