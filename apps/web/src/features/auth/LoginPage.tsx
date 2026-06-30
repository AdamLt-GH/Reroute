import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { useLogin, useRegister } from "./api";

type AuthMode = "login" | "register";

export function LoginPage() {
  const [mode, setMode] = useState<AuthMode>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const login = useLogin();
  const register = useRegister();
  const navigate = useNavigate();
  const location = useLocation();
  const locationState: unknown = location.state;
  const requestedPath =
    typeof locationState === "object" &&
    locationState !== null &&
    "from" in locationState &&
    typeof locationState.from === "string"
      ? locationState.from
      : "/";
  const activeRequest = mode === "login" ? login : register;

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    try {
      if (mode === "login") {
        await login.mutateAsync({ email, password });
      } else {
        await register.mutateAsync({
          email,
          password,
          display_name: displayName,
        });
      }
    } catch {
      // the request error is shown below the form
      return;
    }

    void navigate(requestedPath, { replace: true });
  }

  function changeMode(nextMode: AuthMode) {
    setMode(nextMode);
    login.reset();
    register.reset();
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <p className="eyebrow">Reroute</p>
        <h1>{mode === "login" ? "Sign in" : "Create account"}</h1>
        <p>Use a local account to keep your schedule on this Mac.</p>

        <div className="auth-mode" aria-label="Authentication choice">
          <button
            aria-label="Show login form"
            aria-pressed={mode === "login"}
            onClick={() => changeMode("login")}
            type="button"
          >
            Login
          </button>
          <button
            aria-label="Show registration form"
            aria-pressed={mode === "register"}
            onClick={() => changeMode("register")}
            type="button"
          >
            Register
          </button>
        </div>

        <form
          aria-label={mode === "login" ? "Login form" : "Registration form"}
          className="auth-form"
          onSubmit={(event) => void submit(event)}
        >
          {mode === "register" && (
            <label>
              Display name
              <input
                autoComplete="name"
                maxLength={100}
                onChange={(event) => setDisplayName(event.target.value)}
                required
                value={displayName}
              />
            </label>
          )}

          <label>
            Email
            <input
              autoComplete="email"
              onChange={(event) => setEmail(event.target.value)}
              required
              type="email"
              value={email}
            />
          </label>

          <label>
            Password
            <input
              autoComplete={
                mode === "login" ? "current-password" : "new-password"
              }
              minLength={mode === "register" ? 10 : 1}
              onChange={(event) => setPassword(event.target.value)}
              required
              type="password"
              value={password}
            />
          </label>

          {mode === "register" && (
            <p className="field-help">Use at least 10 characters.</p>
          )}
          {activeRequest.error && (
            <p role="alert">{activeRequest.error.message}</p>
          )}

          <button disabled={activeRequest.isPending} type="submit">
            {activeRequest.isPending
              ? "Please wait..."
              : mode === "login"
                ? "Login"
                : "Register"}
          </button>
        </form>
      </section>
    </main>
  );
}
