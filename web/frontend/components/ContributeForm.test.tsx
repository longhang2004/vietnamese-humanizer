import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, expect, test, vi } from "vitest";
import { ContributeForm } from "./ContributeForm";
import { submitContribution } from "../lib/api";

vi.mock("../lib/api", () => ({ submitContribution: vi.fn() }));

beforeEach(() => vi.resetAllMocks());

function fillExample() {
  fireEvent.change(screen.getByRole("textbox", { name: /^Văn bản gốc/ }), {
    target: { value: "Bản gốc." },
  });
  fireEvent.change(
    screen.getByRole("textbox", { name: /^Bản sửa bạn đề xuất/ }),
    {
      target: { value: "Bản đề xuất." },
    },
  );
  fireEvent.click(screen.getByRole("checkbox"));
}

test("fallback skill choices and multiline context remain usable before metadata arrives", () => {
  render(<ContributeForm skills={[]} />);
  expect(
    screen.getByRole("combobox", { name: /^Ví dụ này cần sửa gì\?/ }),
  ).toHaveValue("humanizer-vi");
  expect(screen.getAllByRole("option")).toHaveLength(4);
  expect(
    screen.getByRole("textbox", { name: "Ngữ cảnh (không bắt buộc)" }).tagName,
  ).toBe("TEXTAREA");
  expect(
    screen.getByRole("textbox", { name: "Ghi chú (không bắt buộc)" }).tagName,
  ).toBe("TEXTAREA");
  expect(screen.getByRole("textbox", { name: /^Văn bản gốc/ })).toHaveAttribute(
    "maxlength",
    "20000",
  );
  expect(
    screen.getByRole("textbox", { name: "Ngữ cảnh (không bắt buộc)" }),
  ).toHaveAttribute("maxlength", "5000");
});

test("failed submission announces the problem and preserves the example for retry", async () => {
  const user = userEvent.setup();
  vi.mocked(submitContribution).mockRejectedValue(
    new Error("Máy chủ chưa phản hồi."),
  );
  render(<ContributeForm skills={[]} />);
  fillExample();
  await user.click(screen.getByRole("button", { name: "Gửi ví dụ" }));
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Máy chủ chưa phản hồi.",
  );
  expect(screen.getByRole("textbox", { name: /^Văn bản gốc/ })).toHaveValue(
    "Bản gốc.",
  );
  expect(
    screen.getByRole("textbox", { name: /^Bản sửa bạn đề xuất/ }),
  ).toHaveValue("Bản đề xuất.");
  expect(screen.getByRole("button", { name: "Gửi ví dụ" })).toBeEnabled();
});

test("successful submission announces receipt and keeps the contribution payload", async () => {
  const user = userEvent.setup();
  vi.mocked(submitContribution).mockResolvedValue({
    id: "example-1",
    status: "pending",
    message: "Đã nhận ví dụ.",
  });
  render(<ContributeForm skills={[]} />);
  fillExample();
  fireEvent.change(
    screen.getByRole("textbox", { name: "Ngữ cảnh (không bắt buộc)" }),
    { target: { value: "Email nội bộ." } },
  );
  fireEvent.change(
    screen.getByRole("textbox", { name: "Ghi chú (không bắt buộc)" }),
    { target: { value: "Rút gọn câu." } },
  );
  await user.click(screen.getByRole("button", { name: "Gửi ví dụ" }));
  expect(submitContribution).toHaveBeenCalledWith({
    input_text: "Bản gốc.",
    suggestion: "Bản đề xuất.",
    skill: "humanizer-vi",
    context: "Email nội bộ.",
    note: "Rút gọn câu.",
    consent: true,
  });
  expect(await screen.findByRole("status")).toHaveTextContent("Đã nhận ví dụ.");
  expect(screen.getByRole("status")).toHaveTextContent("example-1");
  expect(screen.getByRole("checkbox")).not.toBeChecked();
  expect(screen.getByRole("button", { name: "Gửi ví dụ" })).toBeDisabled();
});

test("a submitting example cannot be edited or submitted twice", async () => {
  const user = userEvent.setup();
  vi.mocked(submitContribution).mockImplementation(
    () => new Promise(() => undefined),
  );
  const { container } = render(<ContributeForm skills={[]} />);
  fillExample();
  await user.click(screen.getByRole("button", { name: "Gửi ví dụ" }));
  expect(screen.getByRole("textbox", { name: /^Văn bản gốc/ })).toBeDisabled();
  fireEvent.submit(container.querySelector("form")!);
  expect(submitContribution).toHaveBeenCalledTimes(1);
});
