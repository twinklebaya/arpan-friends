import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..deps import require_admin
from ..models import (
    CrisisStats,
    FeedItem,
    Person,
    PersonStatus,
    ReviewStatus,
    SourceType,
    SourceUpdate,
    Tip,
)
from ..schemas import PersonCreateIn, PersonUpdateIn, ReviewAction, SourceUpdateIn, StatsUpdateIn
from ..services.ingest import create_pending_source_update

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(require_admin)])


# ---------- Tips review queue ----------

@router.get("/tips")
def list_tips(status: Optional[ReviewStatus] = None, session: Session = Depends(get_session)):
    query = select(Tip)
    if status:
        query = query.where(Tip.status == status)
    tips = session.exec(query.order_by(Tip.created_at.desc())).all()
    return [{**t.model_dump(), "image_paths": json.loads(t.image_paths)} for t in tips]


@router.patch("/tips/{tip_id}")
def review_tip(tip_id: int, action: ReviewAction, session: Session = Depends(get_session)):
    tip = session.get(Tip, tip_id)
    if not tip:
        raise HTTPException(404, "Tip not found")
    if tip.status != ReviewStatus.pending:
        raise HTTPException(400, "Tip already reviewed")

    tip.status = ReviewStatus.approved if action.action == "approve" else ReviewStatus.rejected
    tip.reviewed_at = datetime.utcnow()

    if tip.status == ReviewStatus.approved:
        feed_item = FeedItem(
            feed_type="target",
            title=f"Public tip from {tip.contact_name or 'anonymous submitter'}",
            body=tip.message,
            source_name=tip.contact_name or "Public tip",
            origin="tip",
            tip_id=tip.id,
        )
        session.add(feed_item)

    session.add(tip)
    session.commit()
    return {"ok": True, "status": tip.status}


# ---------- Official-source ingestion queue ----------

@router.post("/source-updates")
async def ingest_source_update(payload: SourceUpdateIn, session: Session = Depends(get_session)):
    return await create_pending_source_update(payload, session)


@router.get("/source-updates")
def list_source_updates(status: Optional[ReviewStatus] = None, session: Session = Depends(get_session)):
    query = select(SourceUpdate)
    if status:
        query = query.where(SourceUpdate.review_status == status)
    return session.exec(query.order_by(SourceUpdate.created_at.desc())).all()


@router.patch("/source-updates/{update_id}")
def review_source_update(update_id: int, action: ReviewAction, session: Session = Depends(get_session)):
    update = session.get(SourceUpdate, update_id)
    if not update:
        raise HTTPException(404, "Source update not found")
    if update.review_status != ReviewStatus.pending:
        raise HTTPException(400, "Already reviewed")

    update.review_status = ReviewStatus.approved if action.action == "approve" else ReviewStatus.rejected
    update.reviewed_at = datetime.utcnow()

    if update.review_status == ReviewStatus.approved:
        feed_item = FeedItem(
            feed_type=update.feed_type_suggestion or "general",
            title=f"Update from {update.source_name}",
            body=update.ai_summary or update.raw_text[:500],
            source_name=update.source_name,
            source_url=update.source_url,
            source_type=update.source_type,
            origin="ingestion",
            source_update_id=update.id,
        )
        session.add(feed_item)

        # A status change only ever lands on a Person record via this
        # explicit admin approval step -- never automatically -- and never
        # from a social-media source, regardless of what was suggested.
        if (
            update.ai_person_match_id
            and update.ai_status_suggestion
            and not (update.ai_status_suggestion == PersonStatus.deceased and update.source_type == SourceType.social_media)
        ):
            person = session.get(Person, update.ai_person_match_id)
            if person:
                person.status = update.ai_status_suggestion
                person.source_name = update.source_name
                person.source_url = update.source_url
                person.confirmed_at = datetime.utcnow()
                person.updated_at = datetime.utcnow()
                if person.status == PersonStatus.deceased:
                    person.photo_url = None  # hard-enforce: never keep a photo for the deceased
                session.add(person)

    session.add(update)
    session.commit()
    return {"ok": True, "status": update.review_status}


# ---------- Public person-submission review queue ----------

@router.get("/persons")
def list_persons_admin(
    review_status: Optional[ReviewStatus] = None, session: Session = Depends(get_session)
):
    query = select(Person)
    if review_status:
        query = query.where(Person.review_status == review_status)
    return session.exec(query.order_by(Person.created_at.desc())).all()


@router.patch("/persons/{person_id}/review")
def review_person(person_id: int, action: ReviewAction, session: Session = Depends(get_session)):
    person = session.get(Person, person_id)
    if not person:
        raise HTTPException(404, "Person not found")
    if person.review_status != ReviewStatus.pending:
        raise HTTPException(400, "Already reviewed")

    person.review_status = ReviewStatus.approved if action.action == "approve" else ReviewStatus.rejected
    if person.status == PersonStatus.deceased:
        person.photo_url = None  # hard-enforce even on a freshly-approved public submission
    person.updated_at = datetime.utcnow()

    session.add(person)
    session.commit()
    return {"ok": True, "review_status": person.review_status}


# ---------- Manual person + stats edits (fallback / corrections) ----------

@router.post("/persons")
def create_person(payload: PersonCreateIn, session: Session = Depends(get_session)):
    person = Person(**payload.model_dump())
    session.add(person)
    session.commit()
    session.refresh(person)
    return person


@router.patch("/persons/{person_id}")
def update_person(person_id: int, payload: PersonUpdateIn, session: Session = Depends(get_session)):
    person = session.get(Person, person_id)
    if not person:
        raise HTTPException(404, "Person not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        if field == "photo_urls":
            value = json.dumps(value)
        setattr(person, field, value)
    if person.status == PersonStatus.deceased:
        person.photo_url = None  # hard-enforce here too, in case of manual edits
        person.photo_urls = "[]"
    person.updated_at = datetime.utcnow()

    session.add(person)
    session.commit()
    session.refresh(person)
    return person


@router.patch("/stats")
def update_stats(payload: StatsUpdateIn, session: Session = Depends(get_session)):
    row = session.exec(select(CrisisStats)).first()
    if not row:
        row = CrisisStats()

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(row, field, value)
    row.updated_at = datetime.utcnow()

    session.add(row)
    session.commit()
    session.refresh(row)
    return row
