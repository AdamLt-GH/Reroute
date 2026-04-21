from datetime import UTC, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class TimezoneError(ValueError):
    pass


def get_timezone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as error:
        raise TimezoneError(f"unknown timezone: {name}") from error


def require_aware(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise TimezoneError("datetime must include a timezone")
    return value


def to_utc(value: datetime) -> datetime:
    return require_aware(value).astimezone(UTC)


def to_local(value: datetime, timezone_name: str) -> datetime:
    return require_aware(value).astimezone(get_timezone(timezone_name))


def localise(
    value: datetime,
    timezone_name: str,
    *,
    fold: int | None = None,
) -> datetime:
    if value.tzinfo is not None:
        raise TimezoneError("local datetime must not already have a timezone")
    if fold not in {None, 0, 1}:
        raise TimezoneError("fold must be 0 or 1")

    timezone = get_timezone(timezone_name)
    first = value.replace(tzinfo=timezone, fold=0)
    second = value.replace(tzinfo=timezone, fold=1)

    first_valid = to_local(to_utc(first), timezone_name).replace(tzinfo=None) == value
    second_valid = to_local(to_utc(second), timezone_name).replace(tzinfo=None) == value

    if not first_valid and not second_valid:
        raise TimezoneError("local datetime does not exist")

    if first.utcoffset() != second.utcoffset():
        if fold is None:
            raise TimezoneError("local datetime is ambiguous")
        return first if fold == 0 else second

    return first
