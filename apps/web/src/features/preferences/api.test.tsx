import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { useConstraints } from "./api";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("loads the current users scheduling constraints", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(
      Response.json([
        {
          id: "constraint-1",
          kind: "maximum_daily_work",
          settings: { minutes: 360 },
          enabled: true,
        },
      ]),
    ),
  );
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  const { result } = renderHook(() => useConstraints(), {
    wrapper: ({ children }) => (
      <QueryClientProvider client={client}>{children}</QueryClientProvider>
    ),
  });

  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  expect(result.current.data?.[0]?.kind).toBe("maximum_daily_work");
});
