from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..database import get_session
from ..models import FeedItem, FeedType

router = APIRouter(prefix="/api/feed", tags=["feed"])


def _list(feed_type: FeedType, session: Session):
    query = select(FeedItem).where(FeedItem.feed_type == feed_type).order_by(FeedItem.published_at.desc())
    return session.exec(query).all()


@router.get("/general")
def general_feed(session: Session = Depends(get_session)):
    return _list(FeedType.general, session)


@router.get("/target")
def target_feed(session: Session = Depends(get_session)):
    return _list(FeedType.target, session)
