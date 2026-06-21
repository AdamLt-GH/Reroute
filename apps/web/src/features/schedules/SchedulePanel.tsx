import { useState } from "react";

import {
  useAcceptSchedule,
  useGenerateSchedule,
  useRecalculateSchedule,
  useSchedules,
} from "./api";

function nextWeek(): { horizon_start: string; horizon_end: string } {
  const start = new Date();
  start.setHours(0, 0, 0, 0);
  const end = new Date(start);
  end.setDate(end.getDate() + 7);
  return {
    horizon_start: start.toISOString(),
    horizon_end: end.toISOString(),
  };
}

export function SchedulePanel() {
  const schedules = useSchedules();
  const generate = useGenerateSchedule();
  const accept = useAcceptSchedule();
  const recalculate = useRecalculateSchedule();
  const [title, setTitle] = useState("");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [formError, setFormError] = useState<string>();
  const schedule = recalculate.data ?? generate.data ?? schedules.data?.[0];
  const timeFormat = new Intl.DateTimeFormat(undefined, {
    weekday: "short",
    hour: "numeric",
    minute: "2-digit",
  });

  function submitDisruption(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (
      !schedule ||
      !title ||
      !start ||
      !end ||
      new Date(start) >= new Date(end)
    ) {
      setFormError("Add a title and a valid time range");
      return;
    }
    recalculate.mutate({
      scheduleId: schedule.id,
      disruption: {
        title,
        start_at: new Date(start).toISOString(),
        end_at: new Date(end).toISOString(),
      },
    });
    setFormError(undefined);
  }

  return (
    <section className="schedule-panel" aria-labelledby="schedule-heading">
      <div className="schedule-header">
        <div>
          <p className="eyebrow">Flexible schedule</p>
          <h2 id="schedule-heading">Generated plan</h2>
        </div>
        <button
          disabled={generate.isPending}
          onClick={() => generate.mutate(nextWeek())}
          type="button"
        >
          {generate.isPending ? "Generating..." : "Generate next 7 days"}
        </button>
      </div>

      {(generate.error ?? schedules.error) && (
        <p role="alert">{(generate.error ?? schedules.error)?.message}</p>
      )}
      {!schedule && !schedules.isPending && (
        <p className="empty-state">No schedule has been generated yet.</p>
      )}

      {schedule && (
        <>
          <div className="schedule-status">
            <span>{schedule.status}</span>
            {schedule.unscheduled_task_ids.length > 0 && (
              <span>
                {schedule.unscheduled_task_ids.length} tasks still need time
              </span>
            )}
          </div>
          <div className="schedule-blocks">
            {schedule.blocks.map((block) => (
              <article key={block.id}>
                <strong>{block.title}</strong>
                <span>
                  {timeFormat.format(new Date(block.start_at))} to{" "}
                  {timeFormat.format(new Date(block.end_at))}
                </span>
              </article>
            ))}
          </div>
          {schedule.status === "proposed" && (
            <button
              disabled={accept.isPending}
              onClick={() => accept.mutate(schedule.id)}
              type="button"
            >
              {accept.isPending ? "Accepting..." : "Accept schedule"}
            </button>
          )}
          <form className="disruption-form" onSubmit={submitDisruption}>
            <h3>Something changed?</h3>
            <label>
              What happened
              <input
                value={title}
                onChange={(event) => setTitle(event.target.value)}
              />
            </label>
            <label>
              Starts
              <input
                type="datetime-local"
                value={start}
                onChange={(event) => setStart(event.target.value)}
              />
            </label>
            <label>
              Ends
              <input
                type="datetime-local"
                value={end}
                onChange={(event) => setEnd(event.target.value)}
              />
            </label>
            {(formError ?? recalculate.error?.message) && (
              <p role="alert">{formError ?? recalculate.error?.message}</p>
            )}
            <button disabled={recalculate.isPending} type="submit">
              {recalculate.isPending
                ? "Recalculating..."
                : "Recalculate schedule"}
            </button>
          </form>
        </>
      )}
    </section>
  );
}
