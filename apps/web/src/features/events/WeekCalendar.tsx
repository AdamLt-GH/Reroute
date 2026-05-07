import { useState } from "react";

import { useEvents } from "./api";

function startOfWeek(value: Date): Date {
  const start = new Date(value);
  start.setHours(0, 0, 0, 0);
  const daysSinceMonday = (start.getDay() + 6) % 7;
  start.setDate(start.getDate() - daysSinceMonday);
  return start;
}

function addDays(value: Date, days: number): Date {
  const result = new Date(value);
  result.setDate(result.getDate() + days);
  return result;
}

function sameDay(first: Date, second: Date): boolean {
  return (
    first.getFullYear() === second.getFullYear() &&
    first.getMonth() === second.getMonth() &&
    first.getDate() === second.getDate()
  );
}

interface WeekCalendarProps {
  referenceDate?: Date;
}

export function WeekCalendar({
  referenceDate = new Date(),
}: WeekCalendarProps) {
  const events = useEvents();
  const [weekStart, setWeekStart] = useState(() => startOfWeek(referenceDate));
  const days = Array.from({ length: 7 }, (_, index) =>
    addDays(weekStart, index),
  );
  const weekEnd = days[6] ?? weekStart;
  const dateFormat = new Intl.DateTimeFormat(undefined, {
    day: "numeric",
    month: "short",
  });
  const timeFormat = new Intl.DateTimeFormat(undefined, {
    hour: "numeric",
    minute: "2-digit",
  });

  return (
    <section className="week-calendar" aria-labelledby="week-heading">
      <div className="calendar-toolbar">
        <div>
          <p className="eyebrow">Week</p>
          <h2 id="week-heading">
            {dateFormat.format(weekStart)} to {dateFormat.format(weekEnd)}
          </h2>
        </div>
        <div className="calendar-actions">
          <button
            onClick={() => setWeekStart(addDays(weekStart, -7))}
            type="button"
          >
            Previous
          </button>
          <button
            onClick={() => setWeekStart(startOfWeek(new Date()))}
            type="button"
          >
            Today
          </button>
          <button
            onClick={() => setWeekStart(addDays(weekStart, 7))}
            type="button"
          >
            Next
          </button>
        </div>
      </div>

      {events.isPending && <p>Loading calendar...</p>}
      {events.error && <p role="alert">{events.error.message}</p>}
      <div className="calendar-grid">
        {days.map((day) => {
          const dayEvents =
            events.data?.filter((event) =>
              sameDay(new Date(event.start_at), day),
            ) ?? [];

          return (
            <section className="calendar-day" key={day.toISOString()}>
              <header>
                <span>
                  {day.toLocaleDateString(undefined, { weekday: "short" })}
                </span>
                <strong>{day.getDate()}</strong>
              </header>
              <div className="calendar-events">
                {dayEvents.map((event) => (
                  <article className="calendar-event" key={event.id}>
                    <strong>{event.title}</strong>
                    <span>
                      {timeFormat.format(new Date(event.start_at))} to{" "}
                      {timeFormat.format(new Date(event.end_at))}
                    </span>
                    {event.location && <span>{event.location}</span>}
                  </article>
                ))}
              </div>
            </section>
          );
        })}
      </div>
    </section>
  );
}
