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

  return "";
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

function getErrorMessage(body: unknown): string {
  if (typeof body !== "object" || body === null || !("detail" in body)) {
    return "server error, please try again";
  }

  if (typeof body.detail === "string") {
    return body.detail;
  }

  if (Array.isArray(body.detail)) {
    const firstError: unknown = body.detail[0];
    if (
      typeof firstError === "object" &&
      firstError !== null &&
      "msg" in firstError &&
      typeof firstError.msg === "string"
    ) {
      return firstError.msg;
    }
  }

  return "server error, please try again";
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
    throw new ApiError(getErrorMessage(body), response.status);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}
