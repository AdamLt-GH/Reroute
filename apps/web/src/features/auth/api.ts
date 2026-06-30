import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { ApiError, apiRequest } from "../../api/client";
import type { User } from "./types";

export const currentUserKey = ["auth", "current-user"] as const;

export interface LoginInput {
  email: string;
  password: string;
}

export interface RegistrationInput extends LoginInput {
  display_name: string;
}

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

export function useLogin() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (credentials: LoginInput) =>
      apiRequest<User>("/api/auth/login", {
        method: "POST",
        body: JSON.stringify(credentials),
      }),
    onSuccess: (user) => {
      client.setQueryData(currentUserKey, user);
    },
  });
}

export function useRegister() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: async (details: RegistrationInput) => {
      await apiRequest<User>("/api/users/register", {
        method: "POST",
        body: JSON.stringify(details),
      });
      return apiRequest<User>("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({
          email: details.email,
          password: details.password,
        }),
      });
    },
    onSuccess: (user) => {
      client.setQueryData(currentUserKey, user);
    },
  });
}

export function useLogout() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: () =>
      apiRequest<void>("/api/auth/logout", {
        method: "POST",
      }),
    onSuccess: () => {
      client.setQueryData(currentUserKey, null);
      client.removeQueries({
        predicate: (query) => query.queryKey[0] !== "auth",
      });
    },
  });
}
