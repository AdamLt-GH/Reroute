import { Navigate, Outlet, useLocation } from "react-router-dom";

import { useCurrentUser } from "./api";

export function RequireAuth() {
  const currentUser = useCurrentUser();
  const location = useLocation();

  if (currentUser.isPending) {
    return <p role="status">Checking your session...</p>;
  }

  if (!currentUser.data) {
    return <Navigate replace state={{ from: location.pathname }} to="/login" />;
  }

  return <Outlet />;
}
