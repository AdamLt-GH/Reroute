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
  })
  .refine((task) => new Date(task.earliestStart) < new Date(task.deadline), {
    message: "Deadline must be after the earliest start",
    path: ["deadline"],
  });

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
    },
  });

  const submit = handleSubmit(async (values) => {
    await createTask.mutateAsync({
      title: values.title,
      description: values.description || undefined,
      estimated_minutes: values.estimatedMinutes,
      earliest_start: new Date(values.earliestStart).toISOString(),
      deadline: new Date(values.deadline).toISOString(),
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

      {createTask.error && <p role="alert">{createTask.error.message}</p>}
      <button disabled={createTask.isPending} type="submit">
        {createTask.isPending ? "Adding task..." : "Add task"}
      </button>
    </form>
  );
}
