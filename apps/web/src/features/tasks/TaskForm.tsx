import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { useCreateTask } from "./api";

const taskSchema = z
  .object({
    title: z.string().trim().min(1, "Add a task title"),
    description: z.string(),
    estimatedMinutes: z.coerce.number().int().positive(),
    earliestStart: z.string().min(1, "Choose an earliest start"),
    deadline: z.string().min(1, "Choose a deadline"),
    minimumSessionMinutes: z.coerce.number().int().positive(),
    preferredSessionMinutes: z.coerce.number().int().positive(),
    maximumSessionMinutes: z.coerce.number().int().positive(),
    splittable: z.boolean(),
    priority: z.enum(["low", "medium", "high", "urgent"]),
    difficulty: z.enum(["low", "medium", "high"]),
    category: z.string(),
  })
  .refine((task) => new Date(task.earliestStart) < new Date(task.deadline), {
    message: "Deadline must be after the earliest start",
    path: ["deadline"],
  })
  .refine(
    (task) =>
      task.minimumSessionMinutes <= task.preferredSessionMinutes &&
      task.preferredSessionMinutes <= task.maximumSessionMinutes,
    {
      message: "Session lengths must go from shortest to longest",
      path: ["maximumSessionMinutes"],
    },
  )
  .refine(
    (task) =>
      task.splittable || task.estimatedMinutes <= task.maximumSessionMinutes,
    {
      message: "This task is too long to fit into one session",
      path: ["splittable"],
    },
  );

type TaskFormInput = z.input<typeof taskSchema>;
type TaskFormValues = z.output<typeof taskSchema>;

export function TaskForm() {
  const createTask = useCreateTask();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<TaskFormInput, unknown, TaskFormValues>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: "",
      description: "",
      estimatedMinutes: 60,
      earliestStart: "",
      deadline: "",
      minimumSessionMinutes: 30,
      preferredSessionMinutes: 60,
      maximumSessionMinutes: 120,
      splittable: true,
      priority: "medium",
      difficulty: "medium",
      category: "",
    },
  });

  const submit = handleSubmit(async (values) => {
    await createTask.mutateAsync({
      title: values.title,
      description: values.description || undefined,
      estimated_minutes: values.estimatedMinutes,
      earliest_start: new Date(values.earliestStart).toISOString(),
      deadline: new Date(values.deadline).toISOString(),
      minimum_session_minutes: values.minimumSessionMinutes,
      preferred_session_minutes: values.preferredSessionMinutes,
      maximum_session_minutes: values.maximumSessionMinutes,
      splittable: values.splittable,
      priority: values.priority,
      difficulty: values.difficulty,
      category: values.category || undefined,
    });
    reset();
  });

  return (
    <form className="form-card" onSubmit={(event) => void submit(event)}>
      <h2>Add flexible task</h2>
      <label>
        Title
        <input {...register("title")} />
      </label>
      {errors.title && <p role="alert">{errors.title.message}</p>}

      <label>
        Description
        <textarea rows={3} {...register("description")} />
      </label>

      <label>
        Estimated minutes
        <input min="1" type="number" {...register("estimatedMinutes")} />
      </label>

      <div className="form-row">
        <label>
          Earliest start
          <input type="datetime-local" {...register("earliestStart")} />
        </label>
        <label>
          Deadline
          <input type="datetime-local" {...register("deadline")} />
        </label>
      </div>
      {errors.deadline && <p role="alert">{errors.deadline.message}</p>}

      <fieldset>
        <legend>Session lengths</legend>
        <div className="form-row form-row-three">
          <label>
            Minimum minutes
            <input
              min="1"
              type="number"
              {...register("minimumSessionMinutes")}
            />
          </label>
          <label>
            Preferred minutes
            <input
              min="1"
              type="number"
              {...register("preferredSessionMinutes")}
            />
          </label>
          <label>
            Maximum minutes
            <input
              min="1"
              type="number"
              {...register("maximumSessionMinutes")}
            />
          </label>
        </div>
        {errors.maximumSessionMinutes && (
          <p role="alert">{errors.maximumSessionMinutes.message}</p>
        )}
        <label className="checkbox-field">
          <input type="checkbox" {...register("splittable")} />
          Can split across sessions
        </label>
        {errors.splittable && <p role="alert">{errors.splittable.message}</p>}
      </fieldset>

      <div className="form-row form-row-three">
        <label>
          Priority
          <select {...register("priority")}>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </label>
        <label>
          Difficulty
          <select {...register("difficulty")}>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </label>
        <label>
          Category
          <input {...register("category")} />
        </label>
      </div>

      {createTask.error && <p role="alert">{createTask.error.message}</p>}
      <button disabled={createTask.isPending} type="submit">
        {createTask.isPending ? "Adding task..." : "Add task"}
      </button>
    </form>
  );
}
