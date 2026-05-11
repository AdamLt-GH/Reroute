import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { expect, it } from "vitest";

import { eventsKey } from "../events/api";
import { tasksKey } from "../tasks/api";
import { Dashboard } from "./Dashboard";

it("summarises upcoming work and deadlines", () => {
  const client = new QueryClient({
    defaultOptions: {
      queries: { staleTime: Number.POSITIVE_INFINITY },
    },
  });
  client.setQueryData(eventsKey, [
    {
      id: "event-1",
      title: "Class",
      start_at: "2026-05-11T21:00:00+10:00",
      end_at: "2026-05-11T23:00:00+10:00",
      location: "Campus",
      recurrence_rule: null,
      travel_before_minutes: 0,
      travel_after_minutes: 0,
      locked: true,
    },
  ]);
  client.setQueryData(tasksKey, [
    {
      id: "task-1",
      title: "Finish report",
      remaining_minutes: 180,
      deadline: "2026-05-12T17:00:00+10:00",
      status: "in_progress",
    },
  ]);

  render(
    <QueryClientProvider client={client}>
      <Dashboard referenceDate={new Date("2026-05-11T20:00:00+10:00")} />
    </QueryClientProvider>,
  );

  expect(screen.getByText("Class")).toBeInTheDocument();
  expect(screen.getByText("Finish report")).toBeInTheDocument();
  expect(screen.getByText("3 hours")).toBeInTheDocument();
});
