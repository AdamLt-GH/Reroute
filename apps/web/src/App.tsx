import { useState } from "react";
import { Link, Outlet } from "react-router-dom";

import { useCurrentUser } from "./features/auth/api";
import { AvailabilityEditor } from "./features/availability/AvailabilityEditor";
import { Dashboard } from "./features/dashboard/Dashboard";
import { EventForm } from "./features/events/EventForm";
import { WeekCalendar } from "./features/events/WeekCalendar";
import type { FixedEvent } from "./features/events/api";
import { SettingsEditor } from "./features/preferences/SettingsEditor";
import { SchedulePanel } from "./features/schedules/SchedulePanel";
import { TaskDependencyEditor } from "./features/tasks/TaskDependencyEditor";
import { TaskForm } from "./features/tasks/TaskForm";
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
      <Dashboard />
    </main>
  );
}

export function TasksPage() {
  return (
    <main className="page">
      <h1>Tasks</h1>
      <p>Keep track of flexible work before it is placed into your week.</p>
      <TaskForm />
      <TaskList />
      <TaskDependencyEditor />
    </main>
  );
}

export function CalendarPage() {
  const [editingEvent, setEditingEvent] = useState<FixedEvent>();

  return (
    <main className="page">
      <h1>Calendar</h1>
      <p>Your fixed events and generated schedule will appear here.</p>
      <WeekCalendar onEdit={setEditingEvent} />
      <SchedulePanel />
      <EventForm
        event={editingEvent}
        key={editingEvent?.id ?? "new"}
        onDone={() => setEditingEvent(undefined)}
      />
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
      <p>Set the hard rules and softer goals used to build your schedule.</p>
      <SettingsEditor />
    </main>
  );
}
