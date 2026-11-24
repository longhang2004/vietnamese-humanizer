import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test, vi } from "vitest";
import { GettingStarted } from "./GettingStarted";

test("offers a usable ChatGPT prompt while the plugin has no public listing", () => {
  render(<GettingStarted />);
  expect(screen.getByRole("link", { name: /Mở ChatGPT/ })).toHaveAttribute(
    "href",
    "https://chatgpt.com/",
  );
  expect(
    screen.queryByRole("link", { name: "Cài plugin trong ChatGPT" }),
  ).not.toBeInTheDocument();
  expect(
    screen.getByLabelText<HTMLTextAreaElement>("Yêu cầu mẫu").value,
  ).toContain("Giữ nguyên dữ kiện");
  expect(
    screen.getByLabelText<HTMLTextAreaElement>("Yêu cầu mẫu").value,
  ).toContain("Đoạn mẫu giọng viết của tôi");
});

test.each(["Claude", "Gemini"])(
  "downloads the selected skill for %s",
  async (label) => {
    const user = userEvent.setup();
    render(<GettingStarted />);
    await user.click(screen.getByRole("button", { name: label }));
    await user.selectOptions(
      screen.getByLabelText(/Việc cần làm/),
      "grammar-checker-vi",
    );
    expect(
      screen.getByRole("link", { name: /Tải skill “Soát lỗi tiếng Việt”/ }),
    ).toHaveAttribute(
      "href",
      `/downloads/${label.toLowerCase()}/grammar-checker-vi.zip`,
    );
    expect(
      screen.getByLabelText<HTMLTextAreaElement>("Yêu cầu mẫu").value,
    ).toContain("Soát chính tả");
  },
);

test("copies the chosen task and clears confirmation when the task changes", async () => {
  const user = userEvent.setup();
  const write = vi.spyOn(navigator.clipboard, "writeText").mockResolvedValue();
  render(<GettingStarted />);
  await user.selectOptions(
    screen.getByLabelText(/Việc cần làm/),
    "translationese-cleaner-vi",
  );
  await user.click(screen.getByRole("button", { name: "Sao chép yêu cầu" }));
  expect(write).toHaveBeenCalledWith(
    expect.stringContaining("sửa cấu trúc dịch sát tiếng Anh"),
  );
  expect(screen.getByRole("status")).toHaveTextContent("Đã sao chép");
  await user.selectOptions(
    screen.getByLabelText(/Việc cần làm/),
    "humanizer-vi",
  );
  expect(screen.getByRole("status")).toBeEmptyDOMElement();
});

test("keeps the prompt available for manual copying when clipboard permission is denied", async () => {
  const user = userEvent.setup();
  vi.spyOn(navigator.clipboard, "writeText").mockRejectedValue(
    new Error("denied"),
  );
  render(<GettingStarted />);
  await user.click(screen.getByRole("button", { name: "Sao chép yêu cầu" }));
  expect(screen.getByRole("status")).toHaveTextContent("sao chép trực tiếp");
  expect(
    screen.getByLabelText<HTMLTextAreaElement>("Yêu cầu mẫu").value,
  ).toContain("[Dán văn bản của bạn vào đây]");
});

test("switching to another chatbot offers a guide without a stale native download", async () => {
  const user = userEvent.setup();
  render(<GettingStarted />);
  await user.click(screen.getByRole("button", { name: "Claude" }));
  await user.click(screen.getByRole("button", { name: "Chatbot khác" }));
  expect(
    screen.queryByRole("link", { name: /Tải skill/ }),
  ).not.toBeInTheDocument();
  expect(
    screen.getByRole("link", { name: "Tải bộ hướng dẫn đầy đủ" }),
  ).toHaveAttribute("href", "/downloads/huong-dan-tieng-viet.md");
  expect(
    screen.getByRole("button", { name: "Sao chép yêu cầu" }),
  ).toBeEnabled();
});

test("selecting a scenario preset appends context to the starter prompt", async () => {
  const user = userEvent.setup();
  render(<GettingStarted />);
  await user.selectOptions(
    screen.getByLabelText("Tình huống mẫu (tùy chọn)"),
    "satire",
  );
  expect(
    screen.getByLabelText<HTMLTextAreaElement>("Yêu cầu mẫu").value,
  ).toContain("Văn trào phúng, châm biếm");
});
