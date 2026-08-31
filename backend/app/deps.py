from fastapi import Header, HTTPException, status

from .config import get_settings


def require_admin(authorization: str = Header(default="")) -> None:
    settings = get_settings()
    expected = f"Bearer {settings.admin_token}"
    if not authorization or authorization != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")


def require_ingest_token(authorization: str = Header(default="")) -> None:
    settings = get_settings()
    if not settings.ingest_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="INGEST_TOKEN not configured on this server",
        )
    expected = f"Bearer {settings.ingest_token}"
    if not authorization or authorization != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid ingest token")
