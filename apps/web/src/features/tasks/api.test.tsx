import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { useTasks } from "./api";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("loads the current users tasks", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(
      Response.json([
        {
          id: "task-1",
          title: "Finish report",
          status: "backlog",
        },
      ]),
    ),
  );
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  const { result } = renderHook(() => useTasks(), {
    wrapper: ({ children }) => (
      <QueryClientProvider client={client}>{children}</QueryClientProvider>
    ),
  });

  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  expect(result.current.data?.[0]?.title).toBe("Finish report");
  expect(fetch).toHaveBeenCalledWith(
    "http://localhost:8000/api/tasks",
    expect.objectContaining({ credentials: "include" }),
  );
});
