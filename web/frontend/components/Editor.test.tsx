import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";
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
