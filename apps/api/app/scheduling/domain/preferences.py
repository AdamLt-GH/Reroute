from enum import StrEnum


class ConstraintKind(StrEnum):
    SLEEP_WINDOW = "sleep_window"
    MAXIMUM_DAILY_WORK = "maximum_daily_work"
    UNAVAILABLE_PERIOD = "unavailable_period"


class PreferenceKind(StrEnum):
    AVOID_LATE_WORK = "avoid_late_work"
    COMPACT_DAYS = "compact_days"
    ENERGY_AWARE = "energy_aware"
    PRESERVE_FREE_EVENINGS = "preserve_free_evenings"
    REDUCE_CONTEXT_SWITCHING = "reduce_context_switching"
    SCHEDULE_STABILITY = "schedule_stability"
