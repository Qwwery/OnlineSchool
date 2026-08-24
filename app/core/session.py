import secrets 
from datetime import datetime, timedelta, timezone


def generate_session_id():
    return secrets.token_urlsafe(32)

def get_session_expiry(days: int = 7) -> datetime:
    return lambda: datetime.now(timezone.utc) + timedelta(days=days)

