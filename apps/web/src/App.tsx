import { Link, Outlet } from "react-router-dom";

export function App() {
  return (
    <>
      <header className="site-header">
        <Link className="brand" to="/">
          Reroute
        </Link>
        <nav aria-label="Main navigation">
          <Link to="/tasks">Tasks</Link>
          <Link to="/calendar">Calendar</Link>
        </nav>
      </header>
      <Outlet />
    </>
  );
}

export function HomePage() {
  return (
    <main className="welcome">
      <p className="eyebrow">Reroute</p>
      <h1>Build a week that can handle real life.</h1>
      <p>
        Add your commitments, tasks and availability, then let Reroute work out
        a realistic plan.
      </p>
    </main>
  );
}

export function TasksPage() {
  return (
    <main className="page">
      <h1>Tasks</h1>
      <p>Flexible tasks will be managed here.</p>
    </main>
  );
}

export function CalendarPage() {
  return (
    <main className="page">
      <h1>Calendar</h1>
      <p>Your fixed events and generated schedule will appear here.</p>
    </main>
  );
}
