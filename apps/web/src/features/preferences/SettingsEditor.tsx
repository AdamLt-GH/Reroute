import {
  useConstraints,
  useDeleteConstraint,
  useDeletePreference,
  usePreferences,
} from "./api";
import { ConstraintForm } from "./ConstraintForm";
import { PreferenceForm } from "./PreferenceForm";

const labels: Record<string, string> = {
  sleep_window: "Sleep window",
  maximum_daily_work: "Maximum daily work",
  unavailable_period: "Unavailable period",
  avoid_late_work: "Avoid late work",
  compact_days: "Keep work together",
  energy_aware: "Match work to energy",
  preserve_free_evenings: "Preserve free evenings",
  reduce_context_switching: "Reduce context switching",
  schedule_stability: "Keep the schedule stable",
};

function describeConstraint(settings: Record<string, unknown>): string {
  if (typeof settings.minutes === "number") {
    return `${settings.minutes} minutes each day`;
  }
  if (
    typeof settings.start_time === "string" &&
    typeof settings.end_time === "string"
  ) {
    return `${settings.start_time} to ${settings.end_time}`;
  }
  return "Fixed blocked period";
}

export function SettingsEditor() {
  const constraints = useConstraints();
  const preferences = usePreferences();
  const deleteConstraint = useDeleteConstraint();
  const deletePreference = useDeletePreference();

  return (
    <>
      <div className="settings-forms">
        <ConstraintForm />
        <PreferenceForm />
      </div>

      <div className="settings-lists">
        <section className="editor-list" aria-labelledby="constraints-heading">
          <h2 id="constraints-heading">Constraints</h2>
          {constraints.isPending && <p>Loading constraints...</p>}
          {constraints.error && <p role="alert">{constraints.error.message}</p>}
          {constraints.data?.length === 0 && (
            <p className="empty-state">No constraints added yet.</p>
          )}
          {constraints.data?.map((constraint) => (
            <article className="editor-list-item" key={constraint.id}>
              <div>
                <strong>{labels[constraint.kind]}</strong>
                <span>{describeConstraint(constraint.settings)}</span>
              </div>
              <button
                aria-label={`Remove ${labels[constraint.kind]}`}
                disabled={deleteConstraint.isPending}
                onClick={() => deleteConstraint.mutate(constraint.id)}
                type="button"
              >
                Remove
              </button>
            </article>
          ))}
        </section>

        <section className="editor-list" aria-labelledby="preferences-heading">
          <h2 id="preferences-heading">Preferences</h2>
          {preferences.isPending && <p>Loading preferences...</p>}
          {preferences.error && <p role="alert">{preferences.error.message}</p>}
          {preferences.data?.length === 0 && (
            <p className="empty-state">No preferences added yet.</p>
          )}
          {preferences.data?.map((preference) => (
            <article className="editor-list-item" key={preference.id}>
              <div>
                <strong>{labels[preference.kind]}</strong>
                <span>Importance {preference.weight}</span>
              </div>
              <button
                aria-label={`Remove ${labels[preference.kind]}`}
                disabled={deletePreference.isPending}
                onClick={() => deletePreference.mutate(preference.id)}
                type="button"
              >
                Remove
              </button>
            </article>
          ))}
        </section>
      </div>
    </>
  );
}
