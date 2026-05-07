import { useState } from "react";

import {
  type ConstraintInput,
  type ConstraintKind,
  useCreateConstraint,
} from "./api";

const constraintLabels: Record<ConstraintKind, string> = {
  sleep_window: "Sleep window",
  maximum_daily_work: "Maximum daily work",
  unavailable_period: "Unavailable period",
};

function buildSettings(
  kind: ConstraintKind,
  firstValue: string,
  secondValue: string,
): Record<string, unknown> | null {
  if (kind === "maximum_daily_work") {
    const minutes = Number(firstValue);
    return Number.isInteger(minutes) && minutes > 0 && minutes <= 1440
      ? { minutes }
      : null;
  }

  if (kind === "sleep_window") {
    return firstValue && secondValue && firstValue !== secondValue
      ? { start_time: firstValue, end_time: secondValue }
      : null;
  }

  return firstValue &&
    secondValue &&
    new Date(firstValue) < new Date(secondValue)
    ? {
        start_at: new Date(firstValue).toISOString(),
        end_at: new Date(secondValue).toISOString(),
      }
    : null;
}

export function ConstraintForm() {
  const createConstraint = useCreateConstraint();
  const [kind, setKind] = useState<ConstraintKind>("sleep_window");
  const [firstValue, setFirstValue] = useState("");
  const [secondValue, setSecondValue] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const settings = buildSettings(kind, firstValue, secondValue);

    if (!settings) {
      setValidationError("Check the values for this constraint");
      return;
    }

    const constraint: ConstraintInput = {
      kind,
      settings,
      enabled: true,
    };
    await createConstraint.mutateAsync(constraint);
    setFirstValue("");
    setSecondValue("");
    setValidationError(null);
  }

  return (
    <form className="form-card" onSubmit={(event) => void submit(event)}>
      <h2>Add constraint</h2>
      <label>
        Constraint
        <select
          value={kind}
          onChange={(event) => {
            setKind(event.target.value as ConstraintKind);
            setFirstValue("");
            setSecondValue("");
          }}
        >
          {Object.entries(constraintLabels).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </label>

      {kind === "maximum_daily_work" ? (
        <label>
          Maximum minutes per day
          <input
            min="1"
            max="1440"
            type="number"
            value={firstValue}
            onChange={(event) => setFirstValue(event.target.value)}
          />
        </label>
      ) : (
        <div className="form-row">
          <label>
            Starts
            <input
              type={kind === "sleep_window" ? "time" : "datetime-local"}
              value={firstValue}
              onChange={(event) => setFirstValue(event.target.value)}
            />
          </label>
          <label>
            Ends
            <input
              type={kind === "sleep_window" ? "time" : "datetime-local"}
              value={secondValue}
              onChange={(event) => setSecondValue(event.target.value)}
            />
          </label>
        </div>
      )}

      {validationError && <p role="alert">{validationError}</p>}
      {createConstraint.error && (
        <p role="alert">{createConstraint.error.message}</p>
      )}
      <button disabled={createConstraint.isPending} type="submit">
        {createConstraint.isPending ? "Adding constraint..." : "Add constraint"}
      </button>
    </form>
  );
}
