import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";

import { TaskList } from "./TaskList";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("filters the task list by status", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(
      Response.json([
        {
          id: "task-1",
          title: "Finish report",
          description: null,
          estimated_minutes: 180,
          remaining_minutes: 180,
          actual_minutes: 0,
          earliest_start: "2026-05-06T08:00:00Z",
          deadline: "2026-05-08T08:00:00Z",
          minimum_session_minutes: 30,
          maximum_session_minutes: 120,
          preferred_session_minutes: 60,
          splittable: true,
          priority: "high",
          difficulty: "medium",
          category: "Study",
          status: "backlog",
        },
        {
          id: "task-2",
          title: "Submit worksheet",
          description: null,
          estimated_minutes: 60,
          remaining_minutes: 0,
          actual_minutes: 50,
          earliest_start: "2026-05-05T08:00:00Z",
          deadline: "2026-05-07T08:00:00Z",
          minimum_session_minutes: 30,
          maximum_session_minutes: 60,
          preferred_session_minutes: 60,
          splittable: false,
          priority: "medium",
          difficulty: "low",
          category: "Study",
          status: "completed",
        },
      ]),
    ),
  );
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  const user = userEvent.setup();

  render(
    <QueryClientProvider client={client}>
      <TaskList />
    </QueryClientProvider>,
  );

  expect(await screen.findByText("Finish report")).toBeInTheDocument();
  expect(screen.getByText("Submit worksheet")).toBeInTheDocument();

  await user.selectOptions(screen.getByLabelText("Status"), "completed");

  expect(screen.queryByText("Finish report")).not.toBeInTheDocument();
  expect(screen.getByText("Submit worksheet")).toBeInTheDocument();
});
