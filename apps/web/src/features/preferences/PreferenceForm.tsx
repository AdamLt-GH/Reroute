import { useState } from "react";

import {
  type PreferenceInput,
  type PreferenceKind,
  useCreatePreference,
} from "./api";

const preferenceLabels: Record<PreferenceKind, string> = {
  avoid_late_work: "Avoid late work",
  compact_days: "Keep work together",
  energy_aware: "Match work to energy",
  preserve_free_evenings: "Preserve free evenings",
  reduce_context_switching: "Reduce context switching",
  schedule_stability: "Keep the schedule stable",
};

export function PreferenceForm() {
  const createPreference = useCreatePreference();
  const [kind, setKind] = useState<PreferenceKind>("schedule_stability");
  const [weight, setWeight] = useState(1);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const preference: PreferenceInput = {
      kind,
      weight,
      settings: {},
      enabled: true,
    };
    await createPreference.mutateAsync(preference);
  }

  return (
    <form className="form-card" onSubmit={(event) => void submit(event)}>
      <h2>Add preference</h2>
      <label>
        Preference
        <select
          value={kind}
          onChange={(event) => setKind(event.target.value as PreferenceKind)}
        >
          {Object.entries(preferenceLabels).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </label>

      <label>
        Importance: {weight}
        <input
          min="0"
          max="10"
          step="0.5"
          type="range"
          value={weight}
          onChange={(event) => setWeight(Number(event.target.value))}
        />
      </label>
      <p className="field-help">
        Higher values make this preference matter more when schedules are
        compared.
      </p>

      {createPreference.error && (
        <p role="alert">{createPreference.error.message}</p>
      )}
      <button disabled={createPreference.isPending} type="submit">
        {createPreference.isPending ? "Adding preference..." : "Add preference"}
      </button>
    </form>
  );
}
