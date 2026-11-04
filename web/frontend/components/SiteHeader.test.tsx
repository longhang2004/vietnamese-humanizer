import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test, vi } from "vitest";
import { SiteHeader } from "./SiteHeader";

vi.mock("next/navigation", () => ({ usePathname: () => "/check" }));

test("Escape closes the navigation and returns focus to its toggle", async () => {
  const user = userEvent.setup();
  render(<SiteHeader stars={60} />);
  await user.click(screen.getByRole("button", { name: "Mở menu" }));
  const navigation = screen.getByRole("navigation", {
    name: "Điều hướng chính",
  });
  within(navigation).getByRole("link", { name: "Soát văn bản" }).focus();
  await user.keyboard("{Escape}");
  const toggle = screen.getByRole("button", { name: "Mở menu" });
  expect(toggle).toHaveAttribute("aria-expanded", "false");
  expect(toggle).toHaveFocus();
});
