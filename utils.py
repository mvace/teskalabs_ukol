from datetime import datetime, timezone


def convert_to_utc_timestamp(date_string):
    dt_aware = datetime.fromisoformat(date_string)
    return int(dt_aware.timestamp())
