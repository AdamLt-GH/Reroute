import { createBrowserRouter } from "react-router-dom";

import {
  App,
  AvailabilityPage,
  CalendarPage,
  HomePage,
  SettingsPage,
  TasksPage,
} from "./App";
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
          {
            path: "availability",
            element: <AvailabilityPage />,
          },
          {
            path: "settings",
            element: <SettingsPage />,
          },
        ],
      },
    ],
  },
]);
