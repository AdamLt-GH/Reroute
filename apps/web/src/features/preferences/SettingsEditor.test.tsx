import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";

import { constraintsKey, preferencesKey } from "./api";
import { SettingsEditor } from "./SettingsEditor";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("shows saved settings and removes a constraint", async () => {
  const request = vi.fn(
    (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
      if (init?.method === "DELETE") {
        return Promise.resolve(new Response(null, { status: 204 }));
      }
      const url =
        typeof input === "string"
          ? input
          : input instanceof URL
            ? input.href
            : input.url;
      return Promise.resolve(
        Response.json(
          url.includes("constraints")
            ? [
                {
                  id: "constraint-1",
                  kind: "sleep_window",
                  settings: { start_time: "23:00", end_time: "07:00" },
                  enabled: true,
                },
              ]
            : [
                {
                  id: "preference-1",
                  kind: "schedule_stability",
                  weight: 3,
                  settings: {},
                  enabled: true,
                },
              ],
        ),
      );
    },
  );
  vi.stubGlobal("fetch", request);
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  client.setQueryData(constraintsKey, [
    {
      id: "constraint-1",
      kind: "sleep_window",
      settings: { start_time: "23:00", end_time: "07:00" },
      enabled: true,
    },
  ]);
  client.setQueryData(preferencesKey, [
    {
      id: "preference-1",
      kind: "schedule_stability",
      weight: 3,
      settings: {},
      enabled: true,
    },
  ]);
  const user = userEvent.setup();

  render(
    <QueryClientProvider client={client}>
      <SettingsEditor />
    </QueryClientProvider>,
  );

  expect(screen.getByText("23:00 to 07:00")).toBeInTheDocument();
  expect(screen.getByText("Importance 3")).toBeInTheDocument();

  await user.click(screen.getByRole("button", { name: "Remove Sleep window" }));

  await waitFor(() =>
    expect(request).toHaveBeenCalledWith(
      "http://localhost:8000/api/scheduling/constraints/constraint-1",
      expect.objectContaining({ method: "DELETE" }),
    ),
  );
});
