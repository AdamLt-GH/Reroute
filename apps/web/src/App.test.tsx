import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, render, screen } from "@testing-library/react";
import type { ReactNode } from "react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { App, HomePage } from "./App";

beforeEach(() => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(Response.json([])));
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

function renderApp(component: ReactNode) {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter>{component}</MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("App", () => {
  it("shows the main navigation", () => {
    renderApp(<App />);

    expect(screen.getByRole("link", { name: "Reroute" })).toHaveAttribute(
      "href",
      "/",
    );
    expect(screen.getByRole("link", { name: "Tasks" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Calendar" })).toBeInTheDocument();
  });

  it("explains what the app is for", () => {
    renderApp(<HomePage />);

    expect(
      screen.getByRole("heading", {
        name: "Your week at a glance",
      }),
    ).toBeInTheDocument();
  });
});
