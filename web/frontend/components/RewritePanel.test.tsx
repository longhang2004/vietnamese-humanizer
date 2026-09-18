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
