import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { apiRequest } from "../../api/client";

export interface AvailabilityWindow {
  id: string;
  name: string;
  day_of_week: number;
  start_time: string;
  end_time: string;
  effective_from: string | null;
  effective_until: string | null;
}

export interface AvailabilityInput {
  name: string;
  day_of_week: number;
  start_time: string;
  end_time: string;
  effective_from?: string;
  effective_until?: string;
}

export const availabilityKey = ["availability"] as const;

export function useAvailability() {
  return useQuery({
    queryKey: availabilityKey,
    queryFn: () => apiRequest<AvailabilityWindow[]>("/api/availability"),
  });
}

export function useCreateAvailability() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (window: AvailabilityInput) =>
      apiRequest<AvailabilityWindow>("/api/availability", {
        method: "POST",
        body: JSON.stringify(window),
      }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: availabilityKey });
    },
  });
}

export function useDeleteAvailability() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (windowId: string) =>
      apiRequest<void>(`/api/availability/${windowId}`, {
        method: "DELETE",
      }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: availabilityKey });
    },
  });
}
