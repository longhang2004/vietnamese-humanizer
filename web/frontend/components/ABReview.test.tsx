import {
  act,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, expect, test, vi } from "vitest";
import { ABReview, ABReviewEntry } from "./ABReview";
import { ApiError, fetchHealth } from "../lib/api";
import type { HealthResponse } from "../lib/types";

vi.mock("../lib/api", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../lib/api")>()),
  fetchHealth: vi.fn(),
}));

const session = "22222222-2222-4222-8222-222222222222";
const assignment = {
  id: "33333333-3333-4333-8333-333333333333",
  case_id: "technical",
  topic: "Hướng dẫn kỹ thuật",
  profile: "technical",
  instruction: "Giữ đúng dữ kiện, viết rõ từng bước.",
  input_text: "Bản nháp gốc.\nDòng thứ hai.",
  a: "Đầu ra A.\n<script>không chạy</script>",
  b: "Đầu ra B.\nGiữ nguyên dòng.",
};
const response = {
  session_id: session,
  study: {
    id: "public-pilot",
    version: 1,
    title: "Chấm thử sáu cặp",
    disclosure:
      "Sáu cặp đã công khai, dùng để kiểm tra luồng chấm. Lựa chọn của bạn được lưu để cải thiện bộ skill.",
  },
  assignment,
  completed: 0,
  total: 6,
  skipped: 0,
};
const receipt = {
  id: "receipt",
  message: "Đã lưu lựa chọn.",
  completed: 1,
  total: 6,
  skipped: 0,
};
let requests: { path: string; body: Record<string, unknown> }[];
let health: Record<string, unknown>;
let assign: () => Promise<unknown>;
let vote: () => Promise<unknown>;

function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((done) => {
    resolve = done;
  });
  return { promise, resolve };
}

beforeEach(() => {
  localStorage.clear();
  requests = [];
  health = {
    status: "ok",
    version: "test",
    capabilities: { rewrite: false, contributions: false, ab_review: true },
  };
  assign = async () => response;
  vote = async () => receipt;
  vi.mocked(fetchHealth).mockImplementation(
    async () => health as unknown as HealthResponse,
  );
  vi.stubGlobal(
    "fetch",
    vi.fn(async (url: string, options?: RequestInit) => {
      if (url.endsWith("/api/health"))
        return { ok: true, json: async () => health };
      const path = new URL(url).pathname;
      requests.push({ path, body: JSON.parse(String(options?.body)) });
      const data = path.endsWith("assignments") ? await assign() : await vote();
      return { ok: true, json: async () => data };
    }),
  );
});
afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

test("shows source before neutral verbatim outputs and saves only on explicit submit", async () => {
  const pending = deferred<typeof receipt>();
  vote = () => pending.promise;
  const user = userEvent.setup();
  render(<ABReview />);
  expect(await screen.findByText(assignment.instruction)).toBeInTheDocument();
  const a = screen.getByRole("region", { name: "Bản A" });
  expect(a).toHaveTextContent("<script>không chạy</script>");
  expect(a.querySelector("script")).toBeNull();
  expect(screen.getByText(response.study.disclosure)).toBeInTheDocument();
  expect(
    screen.getByText(/Bản nháp gốc/).compareDocumentPosition(a) &
      Node.DOCUMENT_POSITION_FOLLOWING,
  ).toBeTruthy();
  await user.click(screen.getByRole("radio", { name: "Chọn A" }));
  await user.click(screen.getByRole("checkbox", { name: "Giữ đúng ý" }));
  expect(
    requests.filter((request) => request.path.endsWith("votes")),
  ).toHaveLength(0);
  const submit = screen.getByRole("button", { name: "Gửi lựa chọn" });
  fireEvent.click(submit);
  fireEvent.click(submit);
  expect(requests.filter((request) => request.path.endsWith("votes"))).toEqual([
    {
      path: "/api/ab-review/votes",
      body: {
        session_id: session,
        assignment_id: assignment.id,
        choice: "a",
        reasons: ["meaning"],
      },
    },
  ]);
  expect(screen.queryByText("Đã lưu lựa chọn.")).not.toBeInTheDocument();
  await act(async () => pending.resolve(receipt));
  expect(await screen.findByRole("status")).toHaveTextContent(
    "Đã lưu lựa chọn.",
  );
  assign = async () => ({
    ...response,
    assignment: { ...assignment, id: "next", topic: "Mẫu tiếp theo" },
    completed: 1,
  });
  await user.click(screen.getByRole("button", { name: "Chấm cặp tiếp theo" }));
  expect(
    await screen.findByRole("heading", { name: "Mẫu tiếp theo" }),
  ).toBeInTheDocument();
  expect(requests.at(-1)?.body).toEqual({ session_id: session });
  expect(screen.getByRole("radio", { name: "Chọn A" })).not.toBeChecked();
  expect(screen.getByRole("radio", { name: "Chọn A" })).toBeEnabled();
});

test("retains ballot after network error and retries the identical vote", async () => {
  const user = userEvent.setup();
  vote = async () => {
    throw new Error("Kết nối bị ngắt.");
  };
  render(<ABReview />);
  await user.click(await screen.findByRole("radio", { name: "Chọn B" }));
  await user.click(screen.getByRole("checkbox", { name: "Dễ đọc" }));
  await user.click(screen.getByRole("button", { name: "Gửi lựa chọn" }));
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Kết nối bị ngắt.",
  );
  expect(screen.getByRole("radio", { name: "Chọn B" })).toBeChecked();
  expect(screen.getByRole("checkbox", { name: "Dễ đọc" })).toBeChecked();
  vote = async () => receipt;
  await user.click(screen.getByRole("button", { name: "Gửi lựa chọn" }));
  expect(await screen.findByRole("status")).toHaveTextContent(
    "Đã lưu lựa chọn.",
  );
  const ballots = requests.filter((request) => request.path.endsWith("votes"));
  expect(ballots).toHaveLength(2);
  expect(ballots[1].body).toEqual(ballots[0].body);
});

test("a network failure explains the retry in Vietnamese", async () => {
  const user = userEvent.setup();
  vote = async () => {
    throw new TypeError("Failed to fetch");
  };
  render(<ABReview />);
  await user.click(await screen.findByRole("radio", { name: "Chọn B" }));
  await user.click(screen.getByRole("button", { name: "Gửi lựa chọn" }));
  const alert = await screen.findByRole("alert");
  expect(alert).toHaveTextContent(
    "Chưa kết nối được máy chủ. Bạn hãy thử lại sau. Lựa chọn được giữ; bạn có thể sửa rồi gửi lại.",
  );
  expect(alert).not.toHaveTextContent("Failed to fetch");
});

test("a retryable 5xx hides the raw API detail and stays recoverable", async () => {
  const user = userEvent.setup();
  vote = async () => {
    throw new ApiError("Capability is disabled.", 503);
  };
  render(<ABReview />);
  await user.click(await screen.findByRole("radio", { name: "Chọn A" }));
  await user.click(screen.getByRole("button", { name: "Gửi lựa chọn" }));
  const alert = await screen.findByRole("alert");
  expect(alert).toHaveTextContent("Phần chấm A/B đang tạm nghỉ.");
  expect(alert).not.toHaveTextContent("Capability is disabled.");
  expect(screen.getByRole("button", { name: "Gửi lựa chọn" })).toBeEnabled();
});

test("a 429 names the wait instead of leaking the raw rate-limit text", async () => {
  const user = userEvent.setup();
  vote = async () => {
    throw new ApiError("Rate limit exceeded: 20 per 1 minute.", 429);
  };
  render(<ABReview />);
  await user.click(await screen.findByRole("radio", { name: "Chọn A" }));
  await user.click(screen.getByRole("button", { name: "Gửi lựa chọn" }));
  const alert = await screen.findByRole("alert");
  expect(alert).toHaveTextContent(
    "Bạn đã gửi quá nhiều lượt. Chờ một phút rồi thử lại.",
  );
  expect(alert).not.toHaveTextContent("Rate limit exceeded");
});

test("a closed study does not promise a retry and offers a reload", async () => {
  const user = userEvent.setup();
  vote = async () => {
    throw new ApiError("Đợt chấm này đã đóng.", 409);
  };
  render(<ABReview />);
  await user.click(await screen.findByRole("radio", { name: "Chọn B" }));
  await user.click(screen.getByRole("button", { name: "Gửi lựa chọn" }));
  const alert = await screen.findByRole("alert");
  expect(alert).toHaveTextContent("Đợt chấm này đã đóng.");
  expect(alert).not.toHaveTextContent("gửi lại");
  expect(
    screen.queryByRole("button", { name: "Gửi lựa chọn" }),
  ).not.toBeInTheDocument();
  expect(
    screen.getByText(
      "Lượt này không thể gửi lại. Tải lại để nhận trạng thái mới.",
    ),
  ).toBeInTheDocument();
  expect(screen.getByRole("radio", { name: "Chọn B" })).toBeChecked();
  expect(screen.getByRole("radio", { name: "Chọn A" })).toBeDisabled();
  assign = async () => ({
    ...response,
    assignment: null,
    completed: 6,
    skipped: 1,
  });
  await user.click(screen.getByRole("button", { name: "Tải lại cặp văn bản" }));
  expect(
    await screen.findByRole("heading", { name: "Bạn đã chấm hết các cặp." }),
  ).toBeInTheDocument();
});

test("creates the anonymous session before the first request and keeps persistence copy in the footer only", async () => {
  render(<ABReview />);
  await screen.findByText(assignment.instruction);
  const first = requests[0].body.session_id as string;
  expect(first).toMatch(
    /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i,
  );
  expect(localStorage.getItem("vws:ab-review-session")).toBe(first);
  const heading = screen.getByRole("heading", { name: "Chấm A/B" })
    .nextElementSibling as HTMLElement;
  expect(heading).not.toHaveTextContent("được lưu để cải thiện bộ skill");
  expect(screen.getByText(/Mã phiên ẩn danh/)).toHaveTextContent(
    "Lựa chọn được lưu để cải thiện bộ skill.",
  );
  expect(
    screen.getByText("Về đợt chấm").closest("details"),
  ).not.toHaveAttribute("open");
});

test("a retryable failure keeps the ballot editable and reuses the payload only when unchanged", async () => {
  const user = userEvent.setup();
  vote = async () => {
    throw new Error("Mất phản hồi sau khi lưu.");
  };
  render(<ABReview />);
  await user.click(await screen.findByRole("radio", { name: "Chọn B" }));
  await user.click(screen.getByRole("checkbox", { name: "Giữ đúng ý" }));
  await user.click(screen.getByRole("button", { name: "Gửi lựa chọn" }));
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Mất phản hồi sau khi lưu.",
  );
  expect(screen.getByRole("radio", { name: "Chọn A" })).toBeEnabled();
  expect(screen.getByRole("checkbox", { name: "Dễ đọc" })).toBeEnabled();
  expect(screen.getByRole("radio", { name: "Chọn B" })).toBeChecked();

  // A correction is a new payload rather than a resend of the old vote.
  await user.click(screen.getByRole("radio", { name: "Chọn A" }));
  expect(screen.getByRole("checkbox", { name: "Giữ đúng ý" })).toBeChecked();
  vote = async () => receipt;
  await user.click(screen.getByRole("button", { name: "Gửi lựa chọn" }));
  expect(await screen.findByRole("status")).toHaveTextContent(
    "Đã lưu lựa chọn.",
  );
  expect(requests.filter((request) => request.path.endsWith("votes"))).toEqual([
    {
      path: "/api/ab-review/votes",
      body: {
        session_id: session,
        assignment_id: assignment.id,
        choice: "b",
        reasons: ["meaning"],
      },
    },
    {
      path: "/api/ab-review/votes",
      body: {
        session_id: session,
        assignment_id: assignment.id,
        choice: "a",
        reasons: ["meaning"],
      },
    },
  ]);
});

test("an unchanged retry resends the exact memoized payload", async () => {
  const user = userEvent.setup();
  vote = async () => {
    throw new Error("Mất phản hồi sau khi lưu.");
  };
  render(<ABReview />);
  await user.click(await screen.findByRole("radio", { name: "Chọn B" }));
  await user.click(screen.getByRole("checkbox", { name: "Giữ đúng ý" }));
  await user.click(screen.getByRole("button", { name: "Gửi lựa chọn" }));
  await screen.findByRole("alert");
  vote = async () => receipt;
  await user.click(screen.getByRole("button", { name: "Gửi lựa chọn" }));
  expect(await screen.findByRole("status")).toHaveTextContent(
    "Đã lưu lựa chọn.",
  );
  const ballots = requests.filter((request) => request.path.endsWith("votes"));
  expect(ballots).toHaveLength(2);
  expect(ballots[1].body).toEqual(ballots[0].body);
  expect(
    screen.getByRole("button", { name: "Chấm cặp tiếp theo" }),
  ).toHaveFocus();
});

test("the last receipt focuses the completion heading", async () => {
  const user = userEvent.setup();
  vote = async () => ({ ...receipt, completed: 6, skipped: 1 });
  render(<ABReview />);
  await user.click(await screen.findByRole("radio", { name: "Chọn B" }));
  await user.click(screen.getByRole("button", { name: "Gửi lựa chọn" }));
  expect(
    await screen.findByRole("heading", { name: "Bạn đã chấm hết các cặp." }),
  ).toHaveFocus();
});

test("skip clears reasons and completion reports submitted comparisons separately", async () => {
  const user = userEvent.setup();
  render(<ABReview />);
  await user.click(await screen.findByRole("radio", { name: "Chọn A" }));
  await user.click(screen.getByRole("checkbox", { name: "Dễ đọc" }));
  await user.click(screen.getByRole("radio", { name: "Bỏ qua" }));
  expect(
    screen.queryByRole("checkbox", { name: "Dễ đọc" }),
  ).not.toBeInTheDocument();
  vote = async () => ({ ...receipt, completed: 6, skipped: 2 });
  await user.click(screen.getByRole("button", { name: "Gửi lựa chọn" }));
  expect(requests.at(-1)?.body).toMatchObject({ choice: "skip", reasons: [] });
  expect(
    await screen.findByRole("heading", { name: "Bạn đã chấm hết các cặp." }),
  ).toBeInTheDocument();
  expect(screen.getByText(/4 lượt so sánh.*2 lượt bỏ qua/)).toBeInTheDocument();
  expect(
    screen.queryByRole("button", { name: "Chấm cặp tiếp theo" }),
  ).not.toBeInTheDocument();
});

test("resumes a completed session and uses saved session ID", async () => {
  localStorage.setItem("vws:ab-review-session", session);
  assign = async () => ({
    ...response,
    assignment: null,
    completed: 6,
    skipped: 1,
  });
  render(<ABReview />);
  expect(
    await screen.findByRole("heading", { name: "Bạn đã chấm hết các cặp." }),
  ).toBeInTheDocument();
  expect(requests[0].body).toEqual({ session_id: session });
  expect(screen.getByText(/5 lượt so sánh.*1 lượt bỏ qua/)).toBeInTheDocument();
});

test("blocked storage still keeps an in-memory session for next case", async () => {
  vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
    throw new Error("blocked");
  });
  vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
    throw new Error("blocked");
  });
  const user = userEvent.setup();
  render(<ABReview />);
  await user.click(await screen.findByRole("radio", { name: "Hòa" }));
  await user.click(screen.getByRole("button", { name: "Gửi lựa chọn" }));
  await user.click(
    await screen.findByRole("button", { name: "Chấm cặp tiếp theo" }),
  );
  await waitFor(() =>
    expect(requests.at(-1)?.body).toEqual({ session_id: session }),
  );
});

test("corrupt storage is ignored and a server assignment error can be retried", async () => {
  localStorage.setItem("vws:ab-review-session", "broken-session");
  assign = async () => {
    throw new Error("Đợt chấm đang đóng.");
  };
  const user = userEvent.setup();
  render(<ABReview />);
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Đợt chấm đang đóng.",
  );
  expect(requests[0].body.session_id).not.toBe("broken-session");
  assign = async () => response;
  await user.click(screen.getByRole("button", { name: "Thử tải lại" }));
  expect(
    await screen.findByRole("radio", { name: "Chọn A" }),
  ).toBeInTheDocument();
});

test("stale assignment response after unmount cannot overwrite the current session", async () => {
  const old = deferred<typeof response>();
  assign = () => old.promise;
  const first = render(<ABReview />);
  await waitFor(() => expect(requests).toHaveLength(1));
  first.unmount();
  const currentSession = "44444444-4444-4444-8444-444444444444";
  assign = async () => ({ ...response, session_id: currentSession });
  render(<ABReview />);
  expect(
    await screen.findByRole("radio", { name: "Chọn A" }),
  ).toBeInTheDocument();
  await act(async () => old.resolve(response));
  expect(localStorage.getItem("vws:ab-review-session")).toBe(currentSession);
});

test("examples entry offers the enabled review without requesting a ballot", async () => {
  render(<ABReviewEntry />);
  expect(await screen.findByRole("link", { name: "Chấm A/B" })).toHaveAttribute(
    "href",
    "/review",
  );
  expect(requests).toHaveLength(0);
});

test.each(["loading", "disabled", "old", "unavailable"])(
  "%s capability never loads ballots or offers a review entry",
  async (state) => {
    const pending = deferred<unknown>();
    if (state === "loading") {
      vi.mocked(fetchHealth).mockImplementation(
        () => pending.promise as Promise<HealthResponse>,
      );
    } else if (state === "unavailable") {
      vi.mocked(fetchHealth).mockRejectedValue(new Error("offline"));
    } else {
      health = {
        ...health,
        capabilities: {
          rewrite: false,
          contributions: false,
          ...(state === "disabled" ? { ab_review: false } : {}),
        },
      };
    }
    const { container } = render(
      <>
        <ABReview />
        <ABReviewEntry />
      </>,
    );
    if (state === "loading")
      expect(screen.getByRole("status")).toHaveTextContent(/Đang kiểm tra/);
    else
      expect(
        await screen.findByText(
          state === "unavailable"
            ? /Chưa kết nối được/
            : /Phần chấm A\/B hiện chưa mở/,
        ),
      ).toBeInTheDocument();
    expect(requests).toHaveLength(0);
    expect(screen.queryByRole("radio")).not.toBeInTheDocument();
    expect(
      within(container).queryByRole("link", { name: "Chấm A/B" }),
    ).not.toBeInTheDocument();
  },
);
