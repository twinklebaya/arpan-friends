from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..deps import require_admin
from ..models import HopeComment, HopeEventEngagement, utcnow
from ..schemas import HopeCommentIn, HopeCommentOut, HopeStatsOut

router = APIRouter(prefix="/api/hope", tags=["hope"])


def _get_or_create_engagement(session: Session) -> HopeEventEngagement:
    row = session.exec(select(HopeEventEngagement)).first()
    if row is None:
        row = HopeEventEngagement()
        session.add(row)
        session.commit()
        session.refresh(row)
    return row


@router.get("/stats", response_model=HopeStatsOut)
def get_stats(session: Session = Depends(get_session)):
    row = _get_or_create_engagement(session)
    return HopeStatsOut(love_count=row.love_count)


@router.post("/love", response_model=HopeStatsOut)
def record_love(session: Session = Depends(get_session)):
    row = _get_or_create_engagement(session)
    row.love_count += 1
    row.updated_at = utcnow()
    session.add(row)
    session.commit()
    session.refresh(row)
    return HopeStatsOut(love_count=row.love_count)


@router.get("/comments", response_model=list[HopeCommentOut])
def list_comments(session: Session = Depends(get_session)):
    rows = session.exec(select(HopeComment).order_by(HopeComment.created_at.desc())).all()
    return rows


@router.post("/comments", response_model=HopeCommentOut)
def create_comment(body: HopeCommentIn, session: Session = Depends(get_session)):
    message = body.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Comment can't be empty")
    author_name = (body.author_name or "").strip() or None
    comment = HopeComment(author_name=author_name, message=message[:2000])
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    session: Session = Depends(get_session),
    _admin: None = Depends(require_admin),
):
    comment = session.get(HopeComment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(comment)
    session.commit()
    return {"ok": True}
