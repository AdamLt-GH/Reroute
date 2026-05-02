import { createBrowserRouter } from "react-router-dom";

import { App, CalendarPage, HomePage, TasksPage } from "./App";
import { LoginPage } from "./features/auth/LoginPage";
import { RequireAuth } from "./features/auth/RequireAuth";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    element: <RequireAuth />,
    children: [
      {
        path: "/",
        element: <App />,
        children: [
          {
            index: true,
            element: <HomePage />,
          },
          {
            path: "tasks",
            element: <TasksPage />,
          },
          {
            path: "calendar",
            element: <CalendarPage />,
          },
        ],
      },
    ],
  },
]);
