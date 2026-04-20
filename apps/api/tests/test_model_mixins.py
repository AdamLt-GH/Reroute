from app.models.mixins import TimestampMixin, UuidPrimaryKeyMixin


def test_uuid_mixin_uses_a_uuid_primary_key() -> None:
    column = UuidPrimaryKeyMixin.__annotations__["id"]

    assert "UUID" in str(column)


def test_timestamp_mixin_defines_created_and_updated_times() -> None:
    fields = TimestampMixin.__annotations__

    assert "created_at" in fields
    assert "updated_at" in fields
