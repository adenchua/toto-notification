from datetime import datetime, timezone


def current_datetime_iso():
    return datetime.now(timezone.utc).isoformat()
