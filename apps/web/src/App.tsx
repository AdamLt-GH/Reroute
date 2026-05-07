import { Link, Outlet } from "react-router-dom";

import { useCurrentUser } from "./features/auth/api";
import { AvailabilityEditor } from "./features/availability/AvailabilityEditor";
import { EventForm } from "./features/events/EventForm";
import { TaskList } from "./features/tasks/TaskList";

export function App() {
  const currentUser = useCurrentUser();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Link className="brand" to="/">
          Reroute
        </Link>
        <nav aria-label="Main navigation">
          <Link to="/">Today</Link>
          <Link to="/tasks">Tasks</Link>
          <Link to="/calendar">Calendar</Link>
          <Link to="/availability">Availability</Link>
          <Link to="/settings">Settings</Link>
        </nav>
        <div className="account-summary">
          <strong>{currentUser.data?.display_name}</strong>
          <span>{currentUser.data?.email}</span>
        </div>
      </aside>
      <div className="app-content">
        <header className="page-header">
          <p>Your schedule, with room for real life.</p>
        </header>
        <Outlet />
      </div>
    </div>
  );
}

export function HomePage() {
  return (
    <main className="page">
      <p className="eyebrow">Today</p>
      <h1>Your week at a glance</h1>
      <div className="dashboard-grid">
        <section className="panel">
          <h2>Next up</h2>
          <p>No commitments have been added yet.</p>
        </section>
        <section className="panel">
          <h2>Tasks at risk</h2>
          <p>Tasks close to their deadline will show here.</p>
        </section>
        <section className="panel panel-wide">
          <h2>Workload</h2>
          <p>Add your availability before generating the first schedule.</p>
        </section>
      </div>
    </main>
  );
}

export function TasksPage() {
  return (
    <main className="page">
      <h1>Tasks</h1>
      <p>Keep track of flexible work before it is placed into your week.</p>
      <TaskList />
    </main>
  );
}

export function CalendarPage() {
  return (
    <main className="page">
      <h1>Calendar</h1>
      <p>Your fixed events and generated schedule will appear here.</p>
      <EventForm />
    </main>
  );
}

export function AvailabilityPage() {
  return (
    <main className="page">
      <h1>Availability</h1>
      <p>Choose when flexible work is allowed to be scheduled.</p>
      <AvailabilityEditor />
    </main>
  );
}

export function SettingsPage() {
  return (
    <main className="page">
      <h1>Settings</h1>
      <p>Scheduling rules and preferences will be managed here.</p>
    </main>
  );
}
