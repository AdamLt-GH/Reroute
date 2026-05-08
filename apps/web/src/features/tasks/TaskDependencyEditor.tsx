import { useState } from "react";

import { useTasks } from "./api";
import {
  useCreateTaskDependency,
  useDeleteTaskDependency,
  useTaskDependencies,
} from "./dependenciesApi";

export function TaskDependencyEditor() {
  const tasks = useTasks();
  const dependencies = useTaskDependencies();
  const createDependency = useCreateTaskDependency();
  const deleteDependency = useDeleteTaskDependency();
  const [prerequisiteId, setPrerequisiteId] = useState("");
  const [dependentId, setDependentId] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);
  const taskNames = new Map(
    tasks.data?.map((task) => [task.id, task.title]) ?? [],
  );

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!prerequisiteId || !dependentId) {
      setValidationError("Choose both tasks");
      return;
    }
    if (prerequisiteId === dependentId) {
      setValidationError("A task cannot depend on itself");
      return;
    }

    await createDependency.mutateAsync({
      prerequisite_id: prerequisiteId,
      dependent_id: dependentId,
    });
    setPrerequisiteId("");
    setDependentId("");
    setValidationError(null);
  }

  return (
    <section className="dependency-editor" aria-labelledby="dependency-heading">
      <div>
        <p className="eyebrow">Task order</p>
        <h2 id="dependency-heading">Dependencies</h2>
        <p>
          Choose work that has to be finished before another task can start.
        </p>
      </div>

      <form onSubmit={(event) => void submit(event)}>
        <label>
          Finish first
          <select
            value={prerequisiteId}
            onChange={(event) => setPrerequisiteId(event.target.value)}
          >
            <option value="">Choose a task</option>
            {tasks.data?.map((task) => (
              <option key={task.id} value={task.id}>
                {task.title}
              </option>
            ))}
          </select>
        </label>
        <label>
          Before starting
          <select
            value={dependentId}
            onChange={(event) => setDependentId(event.target.value)}
          >
            <option value="">Choose a task</option>
            {tasks.data?.map((task) => (
              <option key={task.id} value={task.id}>
                {task.title}
              </option>
            ))}
          </select>
        </label>
        <button disabled={createDependency.isPending} type="submit">
          Add dependency
        </button>
      </form>

      {validationError && <p role="alert">{validationError}</p>}
      {createDependency.error && (
        <p role="alert">{createDependency.error.message}</p>
      )}
      {dependencies.error && <p role="alert">{dependencies.error.message}</p>}

      <div className="dependency-list">
        {dependencies.data?.length === 0 && (
          <p className="empty-state">No task dependencies added yet.</p>
        )}
        {dependencies.data?.map((dependency) => (
          <div
            className="dependency-item"
            key={`${dependency.prerequisite_id}:${dependency.dependent_id}`}
          >
            <span>
              <strong>{taskNames.get(dependency.prerequisite_id)}</strong>
              {" before "}
              <strong>{taskNames.get(dependency.dependent_id)}</strong>
            </span>
            <button
              disabled={deleteDependency.isPending}
              onClick={() => deleteDependency.mutate(dependency)}
              type="button"
            >
              Remove
            </button>
          </div>
        ))}
      </div>
    </section>
  );
}
