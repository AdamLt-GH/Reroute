import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { apiRequest } from "../../api/client";

export interface TaskDependency {
  prerequisite_id: string;
  dependent_id: string;
}

export const taskDependenciesKey = ["task-dependencies"] as const;

export function useTaskDependencies() {
  return useQuery({
    queryKey: taskDependenciesKey,
    queryFn: () => apiRequest<TaskDependency[]>("/api/task-dependencies"),
  });
}

export function useCreateTaskDependency() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (dependency: TaskDependency) =>
      apiRequest<TaskDependency>("/api/task-dependencies", {
        method: "POST",
        body: JSON.stringify(dependency),
      }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: taskDependenciesKey });
    },
  });
}

export function useDeleteTaskDependency() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (dependency: TaskDependency) =>
      apiRequest<void>(
        `/api/task-dependencies/${dependency.prerequisite_id}/${dependency.dependent_id}`,
        { method: "DELETE" },
      ),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: taskDependenciesKey });
    },
  });
}
