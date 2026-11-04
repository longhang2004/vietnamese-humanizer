import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";
import { ComparisonExplorer } from "./ComparisonExplorer";

const cases = [
  {
    id: "first",
    topic: "Email",
    tone: "Lịch sự",
    profile: "business",
    prompt: "Sửa email",
    input: "Bản gốc A",
    without: "Đầu ra A",
    with: "Đầu ra B",
  },
  {
    id: "second",
    topic: "Cộng đồng",
    tone: "Gần gũi",
    profile: "social",
    prompt: "Giữ giọng cá nhân",
    input: "Bản gốc C",
    without: "Đầu ra C",
    with: "Đầu ra D",
  },
];

test("switches both genuine outputs and the original request together", async () => {
  const user = userEvent.setup();
  render(<ComparisonExplorer cases={cases} />);
  expect(screen.getByText("Đầu ra A")).toBeInTheDocument();
  await user.selectOptions(screen.getByLabelText("Chủ đề so sánh"), "second");
  expect(screen.queryByText("Đầu ra A")).not.toBeInTheDocument();
  expect(screen.getByText("Đầu ra C")).toBeInTheDocument();
  expect(screen.getByText("Đầu ra D")).toBeInTheDocument();
  await user.click(screen.getByText("Xem yêu cầu và đoạn gốc"));
  expect(screen.getByText("Giữ giọng cá nhân")).toBeVisible();
  expect(screen.getByText("Bản gốc C")).toBeVisible();
});

test("standalone examples use headings directly below the page title", () => {
  render(<ComparisonExplorer cases={cases} headingLevel={2} />);
  expect(
    screen.getByRole("heading", { name: "AI không nạp skill", level: 2 }),
  ).toBeInTheDocument();
  expect(
    screen.getByRole("heading", { name: "AI có nạp skill", level: 2 }),
  ).toBeInTheDocument();
});

test("topic changes announce a short status instead of reading both outputs", async () => {
  const user = userEvent.setup();
  render(<ComparisonExplorer cases={cases} />);
  await user.selectOptions(screen.getByLabelText("Chủ đề so sánh"), "second");
  const status = screen.getByRole("status");
  expect(status).toHaveTextContent("Cộng đồng");
  expect(status).not.toHaveTextContent("Đầu ra C");
  expect(
    screen
      .getByRole("region", { name: "Kết quả AI không nạp skill" })
      .closest("[aria-live]"),
  ).toBeNull();
});
