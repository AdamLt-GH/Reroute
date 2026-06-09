import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { expect, it } from "vitest";

import { schedulesKey } from "./api";
import { SchedulePanel } from "./SchedulePanel";

it("shows a proposed schedule and its unscheduled work", () => {
  const client = new QueryClient({
    defaultOptions: {
      queries: { staleTime: Number.POSITIVE_INFINITY },
    },
  });
  client.setQueryData(schedulesKey, [
    {
      id: "schedule-1",
      status: "proposed",
      source: "initial",
      horizon_start: "2026-06-09T00:00:00Z",
      horizon_end: "2026-06-16T00:00:00Z",
      parent_schedule_id: null,
      unscheduled_task_ids: ["task-2"],
      blocks: [
        {
          id: "block-1",
          task_id: "task-1",
          title: "Finish report",
          start_at: "2026-06-09T09:00:00Z",
          end_at: "2026-06-09T10:00:00Z",
          locked: false,
          completed: false,
        },
      ],
    },
  ]);

  render(
    <QueryClientProvider client={client}>
      <SchedulePanel />
    </QueryClientProvider>,
  );

  expect(screen.getByText("Finish report")).toBeInTheDocument();
  expect(screen.getByText("1 tasks still need time")).toBeInTheDocument();
  expect(
    screen.getByRole("button", { name: "Accept schedule" }),
  ).toBeInTheDocument();
});
