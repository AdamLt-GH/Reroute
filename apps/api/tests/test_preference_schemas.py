import pytest
from pydantic import ValidationError

from app.schemas.preferences import ConstraintCreate, PreferenceCreate


def test_preference_weight_stays_inside_the_supported_range() -> None:
    preference = PreferenceCreate(
        kind="schedule_stability",
        weight=2.5,
    )

    assert preference.weight == 2.5


def test_unknown_constraint_types_are_rejected() -> None:
    with pytest.raises(ValidationError):
        ConstraintCreate(kind="make_everything_perfect")


def test_negative_preference_weights_are_rejected() -> None:
    with pytest.raises(ValidationError):
        PreferenceCreate(
            kind="avoid_late_work",
            weight=-1,
        )
