import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { WeekCalendar } from "./WeekCalendar";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("places fixed events into the selected week", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(
      Response.json([
        {
          id: "event-1",
          title: "Class",
          start_at: "2026-05-08T09:00:00+10:00",
          end_at: "2026-05-08T11:00:00+10:00",
          location: "Campus",
          recurrence_rule: null,
          travel_before_minutes: 20,
          travel_after_minutes: 20,
          locked: true,
        },
      ]),
    ),
  );
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  render(
    <QueryClientProvider client={client}>
      <WeekCalendar referenceDate={new Date("2026-05-08T12:00:00+10:00")} />
    </QueryClientProvider>,
  );

  expect(await screen.findByText("Class")).toBeInTheDocument();
  expect(screen.getByText("Campus")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Previous" })).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Next" })).toBeInTheDocument();
});
