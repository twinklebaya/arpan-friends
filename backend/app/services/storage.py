"""Tip-image storage via Supabase Storage's REST API (a raw HTTP call rather
than the full supabase-py SDK, to keep the dependency footprint small).

This replaces writing to local disk, which doesn't survive a request on a
serverless platform like Vercel (no persistent filesystem between
invocations).
"""

import httpx

from ..config import get_settings


async def upload_image(contents: bytes, storage_path: str, content_type: str) -> str:
    """Upload bytes to the public tip-uploads bucket and return its public URL."""
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise RuntimeError("SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not configured")

    upload_url = (
        f"{settings.supabase_url}/storage/v1/object/"
        f"{settings.supabase_storage_bucket}/{storage_path}"
    )
    headers = {
        "Authorization": f"Bearer {settings.supabase_service_role_key}",
        "Content-Type": content_type,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(upload_url, headers=headers, content=contents)
        resp.raise_for_status()

    return f"{settings.supabase_url}/storage/v1/object/public/{settings.supabase_storage_bucket}/{storage_path}"
