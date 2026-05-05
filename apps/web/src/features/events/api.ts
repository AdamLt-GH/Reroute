import { useMutation, useQueryClient } from "@tanstack/react-query";

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

export function useCreateEvent() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (event: EventInput) =>
      apiRequest("/api/events", {
        method: "POST",
        body: JSON.stringify(event),
      }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: ["events"] });
    },
  });
}
