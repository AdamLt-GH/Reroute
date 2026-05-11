import { useEvents } from "../events/api";
import { useTasks } from "../tasks/api";

interface DashboardProps {
  referenceDate?: Date;
}

export function Dashboard({ referenceDate = new Date() }: DashboardProps) {
  const tasks = useTasks();
  const events = useEvents();
  const activeTasks =
    tasks.data?.filter(
      (task) => task.status !== "completed" && task.status !== "cancelled",
    ) ?? [];
  const riskCutoff = new Date(referenceDate);
  riskCutoff.setHours(riskCutoff.getHours() + 48);
  const tasksAtRisk = activeTasks
    .filter((task) => new Date(task.deadline) <= riskCutoff)
    .sort(
      (first, second) =>
        new Date(first.deadline).getTime() -
        new Date(second.deadline).getTime(),
    );
  const upcomingEvents =
    events.data
      ?.filter((event) => new Date(event.end_at) >= referenceDate)
      .sort(
        (first, second) =>
          new Date(first.start_at).getTime() -
          new Date(second.start_at).getTime(),
      )
      .slice(0, 3) ?? [];
  const remainingMinutes = activeTasks.reduce(
    (total, task) => total + task.remaining_minutes,
    0,
  );
  const dateTimeFormat = new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  });

  return (
    <div className="dashboard-grid">
      <section className="panel">
        <h2>Next up</h2>
        {events.isPending && <p>Loading events...</p>}
        {upcomingEvents.length === 0 && !events.isPending && (
          <p>No upcoming fixed events.</p>
        )}
        <div className="dashboard-list">
          {upcomingEvents.map((event) => (
            <article key={event.id}>
              <strong>{event.title}</strong>
              <span>{dateTimeFormat.format(new Date(event.start_at))}</span>
            </article>
          ))}
        </div>
      </section>

      <section className="panel">
        <h2>Tasks at risk</h2>
        {tasks.isPending && <p>Loading tasks...</p>}
        {tasksAtRisk.length === 0 && !tasks.isPending && (
          <p>No deadlines in the next 48 hours.</p>
        )}
        <div className="dashboard-list">
          {tasksAtRisk.slice(0, 3).map((task) => (
            <article key={task.id}>
              <strong>{task.title}</strong>
              <span>{task.remaining_minutes} minutes left</span>
            </article>
          ))}
        </div>
      </section>

      <section className="panel panel-wide workload-panel">
        <div>
          <h2>Remaining workload</h2>
          <p>Flexible work that still needs a place in the schedule.</p>
        </div>
        <strong>{Math.round((remainingMinutes / 60) * 10) / 10} hours</strong>
      </section>
    </div>
  );
}
