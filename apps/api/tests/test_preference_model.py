from app.models.preference import SchedulingConstraint, SchedulingPreference


def test_preferences_have_a_configurable_weight() -> None:
    weight = SchedulingPreference.__table__.c.weight

    assert weight.default is not None
    assert weight.default.arg == 1.0


def test_constraints_and_preferences_are_owned_by_a_user() -> None:
    assert SchedulingConstraint.__table__.c.user_id.index
    assert SchedulingPreference.__table__.c.user_id.index
