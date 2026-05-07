import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";

import { PreferenceForm } from "./PreferenceForm";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("submits a weighted scheduling preference", async () => {
  const request = vi.fn().mockResolvedValue(
    Response.json({
      id: "preference-1",
      kind: "schedule_stability",
      weight: 4,
      settings: {},
      enabled: true,
    }),
  );
  vi.stubGlobal("fetch", request);
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  const user = userEvent.setup();

  render(
    <QueryClientProvider client={client}>
      <PreferenceForm />
    </QueryClientProvider>,
  );

  const weight = screen.getByLabelText("Importance: 1");
  fireEvent.change(weight, { target: { value: "4" } });
  await user.click(screen.getByRole("button", { name: "Add preference" }));

  await waitFor(() => expect(request).toHaveBeenCalledOnce());
  const call = request.mock.calls[0] as [string, RequestInit];
  expect(call[1].body).toBe(
    JSON.stringify({
      kind: "schedule_stability",
      weight: 4,
      settings: {},
      enabled: true,
    }),
  );
});
