import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, expect, test, vi } from "vitest";
import { RewritePanel } from "./RewritePanel";
import { rewriteText } from "../lib/api";

vi.mock("../lib/api", () => ({
  rewriteText: vi.fn(),
}));

beforeEach(() => {
  vi.mocked(rewriteText).mockReset();
});

test("clears a previous rewrite when the linted text changes", async () => {
  const user = userEvent.setup();
  vi.mocked(rewriteText).mockResolvedValue({
    rewrite: "Bản viết lại của văn bản A",
    review_status: "unreviewed",
    disclaimer: "Cần tác giả duyệt",
  });

  const { rerender } = render(
    <RewritePanel originalText="Văn bản A" issueIds={["VI-HUM-L02"]} />
  );
  await user.click(screen.getByRole("button", { name: /Viết lại bằng Gemini/i }));
  expect(await screen.findByText("Bản viết lại của văn bản A")).toBeInTheDocument();

  rerender(<RewritePanel originalText="Văn bản B" issueIds={["VI-GRA-L01"]} />);
  expect(screen.queryByText("Bản viết lại của văn bản A")).not.toBeInTheDocument();
});

test("ignores a late rewrite response after the input has changed", async () => {
  const user = userEvent.setup();
  let resolveRewrite: (value: {
    rewrite: string;
    review_status: string;
    disclaimer: string;
  }) => void = () => undefined;
  vi.mocked(rewriteText).mockImplementation(
    () =>
      new Promise((resolve) => {
        resolveRewrite = resolve;
      })
  );

  const { rerender, container } = render(
    <RewritePanel originalText="Văn bản A" issueIds={["VI-HUM-L02"]} />
  );
  await user.click(
    screen.getByRole("button", { name: /Viết lại bằng Gemini/i })
  );
  rerender(<RewritePanel originalText="Văn bản B" issueIds={["VI-GRA-L01"]} />);
  resolveRewrite({
    rewrite: "Bản viết lại trễ của A",
    review_status: "unreviewed",
    disclaimer: "Cần tác giả duyệt",
  });

  await Promise.resolve();
  expect(container.textContent).not.toContain("Bản viết lại trễ của A");
});

test("sends the selected voice, relationship and context", async () => {
  const user = userEvent.setup();
  vi.mocked(rewriteText).mockResolvedValue({
    rewrite: "Bạn gửi bản nháp giúp mình.", output_mode: "clean_rewrite", comments: [],
    review_status: "unreviewed", disclaimer: "Cần duyệt",
  });
  render(<RewritePanel originalText="Vui lòng gửi bản nháp." />);
  await user.click(screen.getByText("Chọn giọng và ngữ cảnh (tùy chọn)"));
  await user.selectOptions(screen.getByLabelText("Kênh sử dụng"), "chat");
  await user.selectOptions(screen.getByLabelText("Giọng mong muốn"), "friendly");
  await user.type(screen.getByLabelText("Quan hệ giao tiếp"), "Đồng nghiệp cùng nhóm");
  await user.type(screen.getByLabelText("Cách xưng hô"), "mình–bạn");
  await user.type(screen.getByLabelText("Ngữ cảnh bổ sung"), "Hạn là 15:00");
  await user.click(screen.getByRole("checkbox"));
  await user.click(screen.getByRole("button", { name: /Viết lại bằng Gemini/i }));
  expect(rewriteText).toHaveBeenCalledWith("Vui lòng gửi bản nháp.", "humanizer-vi", undefined, {
    context: "Hạn là 15:00",
    style: expect.objectContaining({
      channel: "chat", register: "friendly", relationship: "Đồng nghiệp cùng nhóm",
      pronouns: "mình–bạn", reduce_hype: true,
    }),
  });
});

test.each(["review_comment", "needs_author_decision"] as const)(
  "%s displays comments without offering to copy a replacement", async (output_mode) => {
    const user = userEvent.setup();
    vi.mocked(rewriteText).mockResolvedValue({
      rewrite: "This must never be offered as a replacement.", output_mode,
      comments: ["Ai là người duyệt bản nháp?"], review_status: "unreviewed", disclaimer: "Cần duyệt",
    });
    render(<RewritePanel originalText="Họ sẽ duyệt bản nháp." />);
    await user.click(screen.getByRole("button", { name: /Viết lại bằng Gemini/i }));
    expect(await screen.findByText("Ai là người duyệt bản nháp?")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Sao chép kết quả/i })).not.toBeInTheDocument();
    expect(screen.queryByText("This must never be offered as a replacement.")).not.toBeInTheDocument();
  }
);

test("changing the profile invalidates an in-flight result", async () => {
  const user = userEvent.setup();
  let resolveRewrite!: (value: Awaited<ReturnType<typeof rewriteText>>) => void;
  vi.mocked(rewriteText).mockImplementation(() => new Promise((resolve) => { resolveRewrite = resolve; }));
  render(<RewritePanel originalText="Văn bản cần sửa." />);
  await user.click(screen.getByRole("button", { name: /Viết lại bằng Gemini/i }));
  await user.click(screen.getByText("Chọn giọng và ngữ cảnh (tùy chọn)"));
  await user.selectOptions(screen.getByLabelText("Giọng mong muốn"), "friendly");
  resolveRewrite({ rewrite: "Bản theo profile cũ", review_status: "unreviewed", disclaimer: "Cần duyệt" });
  await Promise.resolve();
  expect(screen.queryByText("Bản theo profile cũ")).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: /Viết lại bằng Gemini/i })).toBeEnabled();
});
