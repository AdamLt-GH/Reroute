import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it } from "vitest";

import { TaskForm } from "./TaskForm";

it("explains when a task deadline is too early", async () => {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  const user = userEvent.setup();

  render(
    <QueryClientProvider client={client}>
      <TaskForm />
    </QueryClientProvider>,
  );

  await user.type(screen.getByLabelText("Title"), "Finish report");
  await user.type(screen.getByLabelText("Earliest start"), "2026-05-09T10:00");
  await user.type(screen.getByLabelText("Deadline"), "2026-05-09T09:00");
  await user.click(screen.getByRole("button", { name: "Add task" }));

  expect(
    await screen.findByText("Deadline must be after the earliest start"),
  ).toBeInTheDocument();
});
