import secrets 
from datetime import datetime, timedelta


def generat_session_id():
    return secrets.token_urlsafe(32)

def get_session_expiry(days: int = 7) -> datetime:
    return datetime.utcnow() + timedelta(days=days)
