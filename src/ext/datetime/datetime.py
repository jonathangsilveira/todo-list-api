from datetime import datetime, timezone


def to_timestamp_millis(value: datetime) -> int:
    """
        Convert from datetime to timestamp milliseconds.
        :param value: Value in datetime.
        :return: Value in milliseconds.
        """
    return int(value.timestamp() * 1000)


def from_timestamp_millis_utc(millis: int) -> datetime:
    """
    Convert from timestamp milliseconds to datetime with UTC timezone.
    :param millis: Value in milliseconds.
    :return: Datetime with UTC timezone.
    """
    timestamp_seconds = millis / 1000
    return datetime.fromtimestamp(timestamp=timestamp_seconds, tz=timezone.utc)
