import { useState } from "react";

import { type TaskStatus, useTasks } from "./api";

type StatusFilter = "all" | TaskStatus;

const statusLabels: Record<TaskStatus, string> = {
  backlog: "Backlog",
  scheduled: "Scheduled",
  in_progress: "In progress",
  completed: "Completed",
  cancelled: "Cancelled",
};

function formatDeadline(value: string): string {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export function TaskList() {
  const tasks = useTasks();
  const [status, setStatus] = useState<StatusFilter>("all");
  const visibleTasks =
    tasks.data?.filter((task) => status === "all" || task.status === status) ??
    [];

  if (tasks.isPending) {
    return <p>Loading tasks...</p>;
  }

  if (tasks.error) {
    return <p role="alert">{tasks.error.message}</p>;
  }

  return (
    <section className="task-section" aria-labelledby="task-list-heading">
      <div className="task-toolbar">
        <div>
          <p className="eyebrow">Flexible work</p>
          <h2 id="task-list-heading">Your tasks</h2>
        </div>
        <label>
          Status
          <select
            value={status}
            onChange={(event) => setStatus(event.target.value as StatusFilter)}
          >
            <option value="all">All tasks</option>
            {Object.entries(statusLabels).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>
      </div>

      {visibleTasks.length === 0 ? (
        <p className="empty-state">No tasks match this status.</p>
      ) : (
        <div className="task-list">
          {visibleTasks.map((task) => (
            <article className="task-card" key={task.id}>
              <div>
                <span className={`status-pill status-${task.status}`}>
                  {statusLabels[task.status]}
                </span>
                <h3>{task.title}</h3>
                {task.description && <p>{task.description}</p>}
              </div>
              <dl>
                <div>
                  <dt>Remaining</dt>
                  <dd>{task.remaining_minutes} minutes</dd>
                </div>
                <div>
                  <dt>Deadline</dt>
                  <dd>{formatDeadline(task.deadline)}</dd>
                </div>
              </dl>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
