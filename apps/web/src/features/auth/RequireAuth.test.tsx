import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { beforeEach, expect, it, vi } from "vitest";

import { useCurrentUser } from "./api";
import { RequireAuth } from "./RequireAuth";

vi.mock("./api", () => ({
  useCurrentUser: vi.fn(),
}));

const currentUserMock = vi.mocked(useCurrentUser);

beforeEach(() => {
  currentUserMock.mockReset();
});

it("redirects a signed out user to login", async () => {
  currentUserMock.mockReturnValue({
    data: null,
    isPending: false,
  } as ReturnType<typeof useCurrentUser>);

  render(
    <MemoryRouter initialEntries={["/tasks"]}>
      <Routes>
        <Route element={<RequireAuth />}>
          <Route path="/tasks" element={<p>Private tasks</p>} />
        </Route>
        <Route path="/login" element={<p>Login page</p>} />
      </Routes>
    </MemoryRouter>,
  );

  expect(await screen.findByText("Login page")).toBeInTheDocument();
});
