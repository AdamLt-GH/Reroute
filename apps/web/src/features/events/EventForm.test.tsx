import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it } from "vitest";

import { EventForm } from "./EventForm";

it("explains when the event end is before its start", async () => {
  const client = new QueryClient();
  render(
    <QueryClientProvider client={client}>
      <EventForm />
    </QueryClientProvider>,
  );
  const user = userEvent.setup();

  await user.type(screen.getByLabelText("Title"), "Class");
  await user.type(screen.getByLabelText("Starts"), "2026-05-05T10:00");
  await user.type(screen.getByLabelText("Ends"), "2026-05-05T09:00");
  await user.click(screen.getByRole("button", { name: "Add event" }));

  expect(
    await screen.findByText("End time must be after the start"),
  ).toBeInTheDocument();
});
