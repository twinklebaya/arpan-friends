from fastapi import Header, HTTPException, status

from .config import get_settings


def require_admin(authorization: str = Header(default="")) -> None:
    settings = get_settings()
    expected = f"Bearer {settings.admin_token}"
    if not authorization or authorization != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")
