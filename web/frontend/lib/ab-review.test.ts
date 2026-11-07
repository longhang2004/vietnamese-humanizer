import { afterEach, expect, test, vi } from "vitest";
import * as api from "./api";

afterEach(() => vi.unstubAllGlobals());

test("review requests send only opaque session and ballot fields", async () => {
  const fetchMock = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ id: "receipt" }),
  });
  vi.stubGlobal("fetch", fetchMock);
  expect(api).toHaveProperty("fetchReviewAssignment");
  await api.fetchReviewAssignment();
  expect(fetchMock).toHaveBeenLastCalledWith(
    expect.stringMatching(/\/api\/ab-review\/assignments$/),
    expect.objectContaining({ method: "POST", body: "{}" }),
  );
  await api.fetchReviewAssignment("session");
  expect(fetchMock.mock.lastCall?.[1].body).toBe('{"session_id":"session"}');
  await api.submitReviewVote({
    session_id: "session",
    assignment_id: "assignment",
    choice: "b",
    reasons: ["meaning"],
  });
  expect(fetchMock).toHaveBeenLastCalledWith(
    expect.stringMatching(/\/api\/ab-review\/votes$/),
    expect.objectContaining({
      method: "POST",
      body: '{"session_id":"session","assignment_id":"assignment","choice":"b","reasons":["meaning"]}',
    }),
  );
});
