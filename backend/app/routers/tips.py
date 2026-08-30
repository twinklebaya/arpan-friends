import json
import os
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlmodel import Session

from ..config import get_settings
from ..database import get_session
from ..models import Tip
from ..schemas import TipCreateResponse
from ..services.openrouter import moderate_tip

router = APIRouter(prefix="/api/tips", tags=["tips"])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_IMAGE_BYTES = 8 * 1024 * 1024
MAX_IMAGES = 5


@router.post("", response_model=TipCreateResponse)
async def submit_tip(
    message: str = Form(..., min_length=1, max_length=5000),
    contact_name: Optional[str] = Form(None),
    contact_email: Optional[str] = Form(None),
    contact_phone: Optional[str] = Form(None),
    images: List[UploadFile] = File(default=[]),
    session: Session = Depends(get_session),
):
    if len(images) > MAX_IMAGES:
        raise HTTPException(400, f"Max {MAX_IMAGES} images per submission")

    settings = get_settings()
    tip_dir = os.path.join(settings.upload_dir, "tips")
    os.makedirs(tip_dir, exist_ok=True)

    stored_paths = []
    for image in images:
        if not image.filename:
            continue
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(400, f"Unsupported image type: {image.content_type}")
        contents = await image.read()
        if len(contents) > MAX_IMAGE_BYTES:
            raise HTTPException(400, "Image exceeds 8MB limit")
        ext = os.path.splitext(image.filename)[1][:10]
        safe_name = f"{uuid.uuid4().hex}{ext}"
        dest_path = os.path.join(tip_dir, safe_name)
        with open(dest_path, "wb") as f:
            f.write(contents)
        stored_paths.append(f"/uploads/tips/{safe_name}")

    moderation = await moderate_tip(message)

    tip = Tip(
        message=message,
        image_paths=json.dumps(stored_paths),
        contact_name=contact_name,
        contact_email=contact_email,
        contact_phone=contact_phone,
        ai_spam_likelihood=moderation.get("spam_likelihood"),
        ai_notes=moderation.get("notes") or moderation.get("ai_error"),
    )
    session.add(tip)
    session.commit()
    session.refresh(tip)

    return TipCreateResponse(id=tip.id)
