import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test, vi } from "vitest";
import { Editor } from "./Editor";

test("skill selector uses native checkboxes", async () => {
  const user = userEvent.setup();
  render(<Editor skills={[]} onLint={() => undefined} loading={false} />);

  const boxes = screen.getAllByRole("checkbox");
  expect(boxes.length).toBeGreaterThan(0);
  expect(boxes[0]).toBeChecked();

  await user.click(boxes[0]);
  expect(boxes[0]).not.toBeChecked();
});

test("submits only the selected skill IDs with the current text", async () => {
  const user = userEvent.setup();
  const onLint = vi.fn();
  render(<Editor skills={[]} onLint={onLint} loading={false} />);
  expect(screen.getAllByRole("checkbox")).toHaveLength(4);
  fireEvent.change(screen.getByRole("textbox"), { target: { value: "Một đoạn tiếng Việt." } });
  await user.click(screen.getAllByRole("checkbox")[0]);
  await user.click(screen.getByRole("button", { name: "Soát văn phong" }));
  expect(onLint).toHaveBeenCalledWith("Một đoạn tiếng Việt.", ["translationese-cleaner-vi", "grammar-checker-vi", "style-guide-vi"]);
});

test("text changes, sample and clear notify the checker", async () => {
  const user = userEvent.setup();
  const onTextChange = vi.fn();
  render(<Editor skills={[]} onLint={() => undefined} loading={false} onTextChange={onTextChange} />);
  fireEvent.change(screen.getByRole("textbox"), { target: { value: "Bản nháp mới" } });
  expect(onTextChange).toHaveBeenLastCalledWith("Bản nháp mới");
  await user.click(screen.getByRole("button", { name: "Thử văn bản mẫu" }));
  expect(onTextChange).toHaveBeenLastCalledWith((screen.getByRole("textbox") as HTMLTextAreaElement).value);
  await user.click(screen.getByRole("button", { name: "Xóa văn bản" }));
  expect(onTextChange).toHaveBeenLastCalledWith("");
});

test("deselecting every skill prevents submission", async () => {
  const user = userEvent.setup();
  const onLint = vi.fn();
  const { container } = render(<Editor skills={[]} onLint={onLint} loading={false} />);
  fireEvent.change(screen.getByRole("textbox"), { target: { value: "Văn bản" } });
  for (const checkbox of screen.getAllByRole("checkbox")) await user.click(checkbox);
  expect(screen.getByRole("button", { name: "Soát văn phong" })).toBeDisabled();
  fireEvent.submit(container.querySelector("form")!);
  expect(onLint).not.toHaveBeenCalled();
});
