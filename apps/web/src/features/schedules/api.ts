import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { apiRequest } from "../../api/client";

export interface ScheduleBlock {
  id: string;
  task_id: string | null;
  title: string;
  start_at: string;
  end_at: string;
  locked: boolean;
  completed: boolean;
}

export interface Schedule {
  id: string;
  horizon_start: string;
  horizon_end: string;
  status: string;
  source: string;
  parent_schedule_id: string | null;
  unscheduled_task_ids: string[];
  blocks: ScheduleBlock[];
}

export const schedulesKey = ["schedules"] as const;

export function useSchedules() {
  return useQuery({
    queryKey: schedulesKey,
    queryFn: () => apiRequest<Schedule[]>("/api/schedules"),
  });
}

export function useGenerateSchedule() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (horizon: { horizon_start: string; horizon_end: string }) =>
      apiRequest<Schedule>("/api/schedules/generate", {
        method: "POST",
        body: JSON.stringify(horizon),
      }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: schedulesKey });
    },
  });
}

export function useAcceptSchedule() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (scheduleId: string) =>
      apiRequest<Schedule>(`/api/schedules/${scheduleId}/accept`, {
        method: "POST",
      }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: schedulesKey });
      await client.invalidateQueries({ queryKey: ["tasks"] });
    },
  });
}
