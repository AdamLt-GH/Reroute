import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { apiRequest } from "../../api/client";

export type TaskStatus =
  | "backlog"
  | "scheduled"
  | "in_progress"
  | "completed"
  | "cancelled";

export interface Task {
  id: string;
  title: string;
  description: string | null;
  estimated_minutes: number;
  remaining_minutes: number;
  actual_minutes: number;
  earliest_start: string;
  deadline: string;
  minimum_session_minutes: number;
  maximum_session_minutes: number;
  preferred_session_minutes: number;
  splittable: boolean;
  priority: "low" | "medium" | "high" | "urgent";
  difficulty: "low" | "medium" | "high";
  category: string | null;
  status: TaskStatus;
}

export interface TaskInput {
  title: string;
  description?: string;
  estimated_minutes: number;
  earliest_start: string;
  deadline: string;
  minimum_session_minutes?: number;
  maximum_session_minutes?: number;
  preferred_session_minutes?: number;
  splittable?: boolean;
  priority?: Task["priority"];
  difficulty?: Task["difficulty"];
  category?: string;
}

export const tasksKey = ["tasks"] as const;

export function useTasks() {
  return useQuery({
    queryKey: tasksKey,
    queryFn: () => apiRequest<Task[]>("/api/tasks"),
  });
}

export function useCreateTask() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (task: TaskInput) =>
      apiRequest<Task>("/api/tasks", {
        method: "POST",
        body: JSON.stringify(task),
      }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: tasksKey });
    },
  });
}
