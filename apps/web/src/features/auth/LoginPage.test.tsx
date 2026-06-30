import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  cleanup,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";

import { LoginPage } from "./LoginPage";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

function renderLoginPage() {
  const client = new QueryClient({
    defaultOptions: {
      mutations: { retry: false },
      queries: { retry: false },
    },
  });

  render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={["/login"]}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<p>Signed in</p>} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

const userResponse = {
  id: "6c071978-33c0-4558-99f4-6b9cd3c93d97",
  email: "adam@example.com",
  display_name: "Adam",
  timezone: "Australia/Sydney",
  created_at: "2026-09-06T09:00:00Z",
};

it("logs into an existing local account", async () => {
  const user = userEvent.setup();
  const fetchMock = vi.fn().mockResolvedValue(Response.json(userResponse));
  vi.stubGlobal("fetch", fetchMock);
  renderLoginPage();

  await user.type(screen.getByLabelText("Email"), "adam@example.com");
  await user.type(screen.getByLabelText("Password"), "a useful password");
  await user.click(
    within(screen.getByRole("form", { name: "Login form" })).getByRole(
      "button",
      { name: "Login" },
    ),
  );

  expect(await screen.findByText("Signed in")).toBeInTheDocument();
  expect(fetchMock).toHaveBeenCalledWith(
    "/api/auth/login",
    expect.objectContaining({ method: "POST" }),
  );
});

it("registers and then logs into a new account", async () => {
  const user = userEvent.setup();
  const fetchMock = vi
    .fn()
    .mockResolvedValueOnce(Response.json(userResponse, { status: 201 }))
    .mockResolvedValueOnce(Response.json(userResponse));
  vi.stubGlobal("fetch", fetchMock);
  renderLoginPage();

  await user.click(
    screen.getByRole("button", { name: "Show registration form" }),
  );
  await user.type(screen.getByLabelText("Display name"), "Adam");
  await user.type(screen.getByLabelText("Email"), "adam@example.com");
  await user.type(screen.getByLabelText("Password"), "a useful password");
  await user.click(
    within(screen.getByRole("form", { name: "Registration form" })).getByRole(
      "button",
      { name: "Register" },
    ),
  );

  expect(await screen.findByText("Signed in")).toBeInTheDocument();
  expect(fetchMock).toHaveBeenCalledTimes(2);
  expect(fetchMock.mock.calls[0]?.[0]).toBe("/api/users/register");
  expect(fetchMock.mock.calls[1]?.[0]).toBe("/api/auth/login");
});

it("shows an incorrect password message", async () => {
  const user = userEvent.setup();
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValue(
        Response.json({ detail: "invalid email or password" }, { status: 401 }),
      ),
  );
  renderLoginPage();

  await user.type(screen.getByLabelText("Email"), "adam@example.com");
  await user.type(screen.getByLabelText("Password"), "wrong password");
  await user.click(
    within(screen.getByRole("form", { name: "Login form" })).getByRole(
      "button",
      { name: "Login" },
    ),
  );

  await waitFor(() => {
    expect(screen.getByRole("alert")).toHaveTextContent(
      "invalid email or password",
    );
  });
});

it("shows when an email is already registered", async () => {
  const user = userEvent.setup();
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValue(
        Response.json(
          { detail: "email is already registered" },
          { status: 409 },
        ),
      ),
  );
  renderLoginPage();

  await user.click(
    screen.getByRole("button", { name: "Show registration form" }),
  );
  await user.type(screen.getByLabelText("Display name"), "Adam");
  await user.type(screen.getByLabelText("Email"), "adam@example.com");
  await user.type(screen.getByLabelText("Password"), "a useful password");
  await user.click(
    within(screen.getByRole("form", { name: "Registration form" })).getByRole(
      "button",
      { name: "Register" },
    ),
  );

  await waitFor(() => {
    expect(screen.getByRole("alert")).toHaveTextContent(
      "email is already registered",
    );
  });
});
