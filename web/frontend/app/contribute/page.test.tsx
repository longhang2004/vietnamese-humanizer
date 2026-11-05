import { act, render, screen } from "@testing-library/react";
import { beforeEach, expect, test, vi } from "vitest";
import ContributePage from "./page";
import { fetchHealth, fetchSkills } from "../../lib/api";
import type { HealthResponse } from "../../lib/types";

vi.mock("../../lib/api", () => ({
  fetchHealth: vi.fn(),
  fetchSkills: vi.fn(),
  submitContribution: vi.fn(),
}));

beforeEach(() => {
  vi.resetAllMocks();
  vi.mocked(fetchSkills).mockResolvedValue({ skills: [] });
});

test("contribution capability loading does not announce the route as closed", async () => {
  let resolveHealth!: (value: HealthResponse) => void;
  vi.mocked(fetchHealth).mockImplementation(
    () =>
      new Promise((resolve) => {
        resolveHealth = resolve;
      }),
  );
  render(<ContributePage />);
  expect(
    screen.getByRole("heading", { level: 1, name: "Góp mẫu văn bản" }),
  ).toBeInTheDocument();
  expect(screen.getByRole("status")).toHaveTextContent(
    "Đang kiểm tra khả năng gửi mẫu",
  );
  expect(
    screen.queryByText(/Phần gửi mẫu hiện chưa mở/),
  ).not.toBeInTheDocument();
  expect(
    screen.queryByRole("button", { name: "Gửi ví dụ" }),
  ).not.toBeInTheDocument();
  await act(async () => {
    resolveHealth({
      status: "ok",
      version: "test",
      capabilities: { rewrite: false, contributions: true },
    });
  });
  expect(
    await screen.findByRole("button", { name: "Gửi ví dụ" }),
  ).toBeInTheDocument();
  expect(
    screen.getByRole("heading", { level: 1, name: "Góp mẫu văn bản" }),
  ).toBeInTheDocument();
});

test("contributions fail closed when health is unavailable", async () => {
  vi.mocked(fetchHealth).mockRejectedValue(new Error("offline"));
  render(<ContributePage />);
  expect(
    await screen.findByText(/Phần gửi mẫu hiện chưa mở/),
  ).toBeInTheDocument();
  expect(
    screen.queryByRole("button", { name: "Gửi ví dụ" }),
  ).not.toBeInTheDocument();
  expect(fetchSkills).not.toHaveBeenCalled();
});
