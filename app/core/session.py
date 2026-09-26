import secrets 
from datetime import datetime, timedelta, timezone


def generate_session_id():
    return secrets.token_urlsafe(32)

def get_session_expiry(days: int = 7) -> datetime:
    """Возвращает момент времени, когда истекает сессия (по умолчанию через 7 дней)."""
    return datetime.now(timezone.utc) + timedelta(days=days)


# Время жизни сессии в секундах (используется для max_age cookie)
SESSION_MAX_AGE_SECONDS = 7 * 24 * 60 * 60

