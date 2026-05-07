import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { useEvents } from "./api";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("loads fixed events for the calendar", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(
      Response.json([
        {
          id: "event-1",
          title: "Class",
          start_at: "2026-05-08T09:00:00Z",
          end_at: "2026-05-08T11:00:00Z",
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

  const { result } = renderHook(() => useEvents(), {
    wrapper: ({ children }) => (
      <QueryClientProvider client={client}>{children}</QueryClientProvider>
    ),
  });

  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  expect(result.current.data?.[0]?.title).toBe("Class");
});
