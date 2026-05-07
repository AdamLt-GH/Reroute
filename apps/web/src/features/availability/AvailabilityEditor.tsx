import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import {
  useAvailability,
  useCreateAvailability,
  useDeleteAvailability,
} from "./api";

const days = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
];

const availabilitySchema = z
  .object({
    name: z.string().trim().min(1, "Add a name for this window"),
    dayOfWeek: z.coerce.number().int().min(0).max(6),
    startTime: z.string().min(1, "Choose a start time"),
    endTime: z.string().min(1, "Choose an end time"),
  })
  .refine((window) => window.startTime < window.endTime, {
    message: "End time must be after the start",
    path: ["endTime"],
  });

type AvailabilityInput = z.input<typeof availabilitySchema>;
type AvailabilityValues = z.output<typeof availabilitySchema>;

export function AvailabilityEditor() {
  const windows = useAvailability();
  const createWindow = useCreateAvailability();
  const deleteWindow = useDeleteAvailability();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<AvailabilityInput, unknown, AvailabilityValues>({
    resolver: zodResolver(availabilitySchema),
    defaultValues: {
      name: "",
      dayOfWeek: 0,
      startTime: "08:00",
      endTime: "17:00",
    },
  });

  const submit = handleSubmit(async (values) => {
    await createWindow.mutateAsync({
      name: values.name,
      day_of_week: values.dayOfWeek,
      start_time: values.startTime,
      end_time: values.endTime,
    });
    reset();
  });

  return (
    <div className="editor-grid">
      <form className="form-card" onSubmit={(event) => void submit(event)}>
        <h2>Add availability</h2>
        <label>
          Name
          <input {...register("name")} />
        </label>
        {errors.name && <p role="alert">{errors.name.message}</p>}

        <label>
          Day
          <select {...register("dayOfWeek")}>
            {days.map((day, index) => (
              <option key={day} value={index}>
                {day}
              </option>
            ))}
          </select>
        </label>

        <div className="form-row">
          <label>
            Starts
            <input type="time" {...register("startTime")} />
          </label>
          <label>
            Ends
            <input type="time" {...register("endTime")} />
          </label>
        </div>
        {errors.endTime && <p role="alert">{errors.endTime.message}</p>}

        {createWindow.error && <p role="alert">{createWindow.error.message}</p>}
        <button disabled={createWindow.isPending} type="submit">
          {createWindow.isPending ? "Adding window..." : "Add window"}
        </button>
      </form>

      <section className="editor-list" aria-labelledby="availability-heading">
        <h2 id="availability-heading">Weekly windows</h2>
        {windows.isPending && <p>Loading availability...</p>}
        {windows.error && <p role="alert">{windows.error.message}</p>}
        {windows.data?.length === 0 && (
          <p className="empty-state">No availability added yet.</p>
        )}
        {windows.data?.map((window) => (
          <article className="editor-list-item" key={window.id}>
            <div>
              <strong>{window.name}</strong>
              <span>
                {days[window.day_of_week]} {window.start_time.slice(0, 5)} to{" "}
                {window.end_time.slice(0, 5)}
              </span>
            </div>
            <button
              disabled={deleteWindow.isPending}
              onClick={() => deleteWindow.mutate(window.id)}
              type="button"
            >
              Remove
            </button>
          </article>
        ))}
      </section>
    </div>
  );
}
