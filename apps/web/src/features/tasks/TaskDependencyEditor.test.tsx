import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it } from "vitest";

import { tasksKey } from "./api";
import { taskDependenciesKey } from "./dependenciesApi";
import { TaskDependencyEditor } from "./TaskDependencyEditor";

it("stops a task from depending on itself", async () => {
  const client = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        staleTime: Number.POSITIVE_INFINITY,
      },
    },
  });
  client.setQueryData(tasksKey, [
    {
      id: "task-1",
      title: "Finish report",
      status: "backlog",
    },
  ]);
  client.setQueryData(taskDependenciesKey, []);
  const user = userEvent.setup();

  render(
    <QueryClientProvider client={client}>
      <TaskDependencyEditor />
    </QueryClientProvider>,
  );

  await user.selectOptions(screen.getByLabelText("Finish first"), "task-1");
  await user.selectOptions(screen.getByLabelText("Before starting"), "task-1");
  await user.click(screen.getByRole("button", { name: "Add dependency" }));

  expect(
    screen.getByText("A task cannot depend on itself"),
  ).toBeInTheDocument();
});
