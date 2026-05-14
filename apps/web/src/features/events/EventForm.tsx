import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { type FixedEvent, useCreateEvent, useUpdateEvent } from "./api";

const eventSchema = z
  .object({
    title: z.string().trim().min(1, "Add an event title"),
    start: z.string().min(1, "Choose a start time"),
    end: z.string().min(1, "Choose an end time"),
    location: z.string(),
    travelBefore: z.coerce.number().int().min(0).max(1440),
    travelAfter: z.coerce.number().int().min(0).max(1440),
  })
  .refine((event) => new Date(event.start) < new Date(event.end), {
    message: "End time must be after the start",
    path: ["end"],
  });

type EventFormInput = z.input<typeof eventSchema>;
type EventFormValues = z.output<typeof eventSchema>;

function toLocalInput(value: string): string {
  const date = new Date(value);
  const offset = date.getTimezoneOffset() * 60_000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 16);
}

interface EventFormProps {
  event?: FixedEvent;
  onDone?: () => void;
}

export function EventForm({ event, onDone }: EventFormProps) {
  const createEvent = useCreateEvent();
  const updateEvent = useUpdateEvent(event?.id ?? "");
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<EventFormInput, unknown, EventFormValues>({
    resolver: zodResolver(eventSchema),
    defaultValues: {
      title: event?.title ?? "",
      start: event ? toLocalInput(event.start_at) : "",
      end: event ? toLocalInput(event.end_at) : "",
      location: event?.location ?? "",
      travelBefore: event?.travel_before_minutes ?? 0,
      travelAfter: event?.travel_after_minutes ?? 0,
    },
  });

  const submit = handleSubmit(async (values) => {
    const request = {
      title: values.title,
      start_at: new Date(values.start).toISOString(),
      end_at: new Date(values.end).toISOString(),
      location: values.location || undefined,
      travel_before_minutes: values.travelBefore,
      travel_after_minutes: values.travelAfter,
      locked: true,
    };
    if (event) {
      await updateEvent.mutateAsync(request);
    } else {
      await createEvent.mutateAsync(request);
    }
    reset();
    onDone?.();
  });

  return (
    <form className="form-card" onSubmit={(event) => void submit(event)}>
      <h2>{event ? "Edit fixed event" : "Add fixed event"}</h2>
      <label>
        Title
        <input {...register("title")} />
      </label>
      {errors.title && <p role="alert">{errors.title.message}</p>}

      <div className="form-row">
        <label>
          Starts
          <input type="datetime-local" {...register("start")} />
        </label>
        <label>
          Ends
          <input type="datetime-local" {...register("end")} />
        </label>
      </div>
      {errors.end && <p role="alert">{errors.end.message}</p>}

      <label>
        Location
        <input {...register("location")} />
      </label>

      <div className="form-row">
        <label>
          Travel before
          <input type="number" {...register("travelBefore")} />
        </label>
        <label>
          Travel after
          <input type="number" {...register("travelAfter")} />
        </label>
      </div>

      {(createEvent.error ?? updateEvent.error) && (
        <p role="alert">{(createEvent.error ?? updateEvent.error)?.message}</p>
      )}
      <button
        disabled={createEvent.isPending || updateEvent.isPending}
        type="submit"
      >
        {event ? "Save event" : "Add event"}
      </button>
      {event && (
        <button className="secondary-button" onClick={onDone} type="button">
          Cancel
        </button>
      )}
    </form>
  );
}
