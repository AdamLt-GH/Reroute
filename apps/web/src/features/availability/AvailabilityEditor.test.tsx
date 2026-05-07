import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";

import { AvailabilityEditor } from "./AvailabilityEditor";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("explains when an availability window is reversed", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(Response.json([])));
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  const user = userEvent.setup();

  render(
    <QueryClientProvider client={client}>
      <AvailabilityEditor />
    </QueryClientProvider>,
  );

  await screen.findByText("No availability added yet.");
  await user.type(screen.getByLabelText("Name"), "Evening study");
  await user.clear(screen.getByLabelText("Starts"));
  await user.type(screen.getByLabelText("Starts"), "20:00");
  await user.clear(screen.getByLabelText("Ends"));
  await user.type(screen.getByLabelText("Ends"), "18:00");
  await user.click(screen.getByRole("button", { name: "Add window" }));

  expect(
    await screen.findByText("End time must be after the start"),
  ).toBeInTheDocument();
});
