import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";

import { ConstraintForm } from "./ConstraintForm";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("submits a maximum daily work constraint", async () => {
  const request = vi.fn().mockResolvedValue(
    Response.json({
      id: "constraint-1",
      kind: "maximum_daily_work",
      settings: { minutes: 360 },
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
      <ConstraintForm />
    </QueryClientProvider>,
  );

  await user.selectOptions(
    screen.getByLabelText("Constraint"),
    "maximum_daily_work",
  );
  await user.type(screen.getByLabelText("Maximum minutes per day"), "360");
  await user.click(screen.getByRole("button", { name: "Add constraint" }));

  await waitFor(() => expect(request).toHaveBeenCalledOnce());
  const call = request.mock.calls[0] as [string, RequestInit];
  expect(call[1].body).toBe(
    JSON.stringify({
      kind: "maximum_daily_work",
      settings: { minutes: 360 },
      enabled: true,
    }),
  );
});
