function getApiUrl(): string {
  const environment: unknown = import.meta.env;

  if (
    typeof environment === "object" &&
    environment !== null &&
    "VITE_API_URL" in environment &&
    typeof environment.VITE_API_URL === "string"
  ) {
    return environment.VITE_API_URL;
  }

  return "http://localhost:8000";
}

const API_URL = getApiUrl();

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
  }
}

export async function apiRequest<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    const body: unknown = await response.json().catch(() => null);
    const message =
      typeof body === "object" &&
      body !== null &&
      "detail" in body &&
      typeof body.detail === "string"
        ? body.detail
        : "request failed";
    throw new ApiError(message, response.status);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}
