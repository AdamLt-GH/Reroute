# Scheduling flow

The basic workflow is:

1. Add tasks, fixed events and weekly availability.
2. Generate a schedule for the next seven days.
3. Review and accept the proposed blocks.
4. Add an unexpected blocked period when plans change.
5. Review the replacement schedule.

The solver removes fixed events and travel time from available windows. It then
places tasks in dependency and deadline order while respecting earliest starts,
session lengths and the daily workload limit.

Each generated result is saved separately. A recalculated schedule points to
the schedule it replaced so the previous plan is not overwritten.
