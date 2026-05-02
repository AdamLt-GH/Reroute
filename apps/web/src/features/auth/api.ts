import { useQuery } from "@tanstack/react-query";

import { ApiError, apiRequest } from "../../api/client";
import type { User } from "./types";

export const currentUserKey = ["auth", "current-user"] as const;

async function getCurrentUser(): Promise<User | null> {
  try {
    return await apiRequest<User>("/api/auth/me");
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      return null;
    }
    throw error;
  }
}

export function useCurrentUser() {
  return useQuery({
    queryKey: currentUserKey,
    queryFn: getCurrentUser,
    staleTime: 60_000,
    retry: false,
  });
}
