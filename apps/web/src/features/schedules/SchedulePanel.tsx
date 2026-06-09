import { useAcceptSchedule, useGenerateSchedule, useSchedules } from "./api";

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
  const schedule = generate.data ?? schedules.data?.[0];
  const timeFormat = new Intl.DateTimeFormat(undefined, {
    weekday: "short",
    hour: "numeric",
    minute: "2-digit",
  });

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
        </>
      )}
    </section>
  );
}
