"""Narrow-scope endpoint for automated feed ingestion (e.g. a scheduled
ChatGPT or Claude task watching for news). Gated by its own INGEST_TOKEN,
deliberately separate from the full admin API/ADMIN_TOKEN -- whoever holds
this token can only submit text for OpenRouter classification into the
*pending* review queue. They cannot list/approve/reject anything, edit a
person, or see tips. A human must still approve every item via /admin
before it reaches a live feed or changes a person's status.
"""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..deps import require_ingest_token
from ..schemas import SourceUpdateIn
from ..services.ingest import create_pending_source_update

router = APIRouter(
    prefix="/api/ingest",
    tags=["ingest"],
    dependencies=[Depends(require_ingest_token)],
)


@router.post("/source-updates")
async def ingest_source_update(payload: SourceUpdateIn, session: Session = Depends(get_session)):
    update = await create_pending_source_update(payload, session)
    return {
        "id": update.id,
        "review_status": update.review_status,
        "ai_summary": update.ai_summary,
        "feed_type_suggestion": update.feed_type_suggestion,
        "message": "Received. This is queued for admin review and will not appear on the site until approved.",
    }
