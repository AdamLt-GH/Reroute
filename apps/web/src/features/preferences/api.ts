import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { apiRequest } from "../../api/client";

export type ConstraintKind =
  | "sleep_window"
  | "maximum_daily_work"
  | "unavailable_period";

export type PreferenceKind =
  | "avoid_late_work"
  | "compact_days"
  | "energy_aware"
  | "preserve_free_evenings"
  | "reduce_context_switching"
  | "schedule_stability";

export interface SchedulingConstraint {
  id: string;
  kind: ConstraintKind;
  settings: Record<string, unknown>;
  enabled: boolean;
}

export interface SchedulingPreference {
  id: string;
  kind: PreferenceKind;
  weight: number;
  settings: Record<string, unknown>;
  enabled: boolean;
}

export type ConstraintInput = Omit<SchedulingConstraint, "id">;
export type PreferenceInput = Omit<SchedulingPreference, "id">;

export const constraintsKey = ["scheduling", "constraints"] as const;
export const preferencesKey = ["scheduling", "preferences"] as const;

export function useConstraints() {
  return useQuery({
    queryKey: constraintsKey,
    queryFn: () =>
      apiRequest<SchedulingConstraint[]>("/api/scheduling/constraints"),
  });
}

export function usePreferences() {
  return useQuery({
    queryKey: preferencesKey,
    queryFn: () =>
      apiRequest<SchedulingPreference[]>("/api/scheduling/preferences"),
  });
}

export function useCreateConstraint() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (constraint: ConstraintInput) =>
      apiRequest<SchedulingConstraint>("/api/scheduling/constraints", {
        method: "POST",
        body: JSON.stringify(constraint),
      }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: constraintsKey });
    },
  });
}

export function useDeleteConstraint() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (constraintId: string) =>
      apiRequest<void>(`/api/scheduling/constraints/${constraintId}`, {
        method: "DELETE",
      }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: constraintsKey });
    },
  });
}

export function useCreatePreference() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (preference: PreferenceInput) =>
      apiRequest<SchedulingPreference>("/api/scheduling/preferences", {
        method: "POST",
        body: JSON.stringify(preference),
      }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: preferencesKey });
    },
  });
}

export function useDeletePreference() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (preferenceId: string) =>
      apiRequest<void>(`/api/scheduling/preferences/${preferenceId}`, {
        method: "DELETE",
      }),
    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: preferencesKey });
    },
  });
}
