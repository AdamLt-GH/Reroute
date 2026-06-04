from app.models.schedule import Schedule, ScheduleBlock


def test_schedules_keep_proposed_blocks_and_revision_links() -> None:
    schedule_columns = Schedule.__table__.c
    block_columns = ScheduleBlock.__table__.c

    assert schedule_columns.user_id.index
    assert schedule_columns.parent_schedule_id.nullable
    assert block_columns.schedule_id.index
    assert block_columns.task_id.nullable
