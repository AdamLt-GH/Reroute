import { createBrowserRouter } from "react-router-dom";

import { App, CalendarPage, HomePage, TasksPage } from "./App";

export const router = createBrowserRouter([
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
]);
