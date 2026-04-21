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
