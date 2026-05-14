import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { apiRequest } from "../../api/client";

export interface EventInput {
  title: string;
  start_at: string;
  end_at: string;
  location?: string;
  travel_before_minutes: number;
  travel_after_minutes: number;
  locked: boolean;
}

export interface FixedEvent extends Omit<EventInput, "location"> {
  id: string;
  location: string | null;
  recurrence_rule: string | null;
}

export const eventsKey = ["events"] as const;

export function useEvents() {
  return useQuery({
    queryKey: eventsKey,
    queryFn: () => apiRequest<FixedEvent[]>("/api/events"),
  });
}

export function useCreateEvent() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (event: EventInput) =>
      apiRequest("/api/events", {
        method: "POST",
        body: JSON.stringify(event),
      }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: eventsKey });
    },
  });
}

export function useUpdateEvent(eventId: string) {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (event: EventInput) =>
      apiRequest<FixedEvent>(`/api/events/${eventId}`, {
        method: "PUT",
        body: JSON.stringify(event),
      }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: eventsKey });
    },
  });
}

export function useDeleteEvent() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (eventId: string) =>
      apiRequest<void>(`/api/events/${eventId}`, { method: "DELETE" }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: eventsKey });
    },
  });
}
