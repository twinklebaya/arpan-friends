import json
from typing import Optional

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..database import get_session
from ..models import Person, PersonStatus, ReviewStatus
from ..schemas import PersonSubmitIn

router = APIRouter(prefix="/api/persons", tags=["persons"])


def _public_person(p: Person) -> dict:
    """Serialize a Person, stripping every photo field whenever status !=
    missing.

    This is the hard enforcement point for "never show a photo of the
    deceased" -- even if photo_url/photo_urls were ever set on a deceased
    record by mistake, they will not leave this function.
    """
    is_missing = p.status == PersonStatus.missing
    data = {
        "id": p.id,
        "name": p.name,
        "age": p.age,
        "is_primary_target": p.is_primary_target,
        "status": p.status,
        "last_seen_location": p.last_seen_location,
        "physical_markers": p.physical_markers,
        "photo_url": p.photo_url if is_missing else None,
        "photo_urls": json.loads(p.photo_urls) if is_missing else [],
    }
    if p.status == PersonStatus.deceased:
        data.update(
            {
                "found_location": p.found_location,
                "source_name": p.source_name,
                "source_url": p.source_url,
                "confirmed_at": p.confirmed_at,
            }
        )
    return data


@router.get("")
def list_persons(status: Optional[PersonStatus] = None, session: Session = Depends(get_session)):
    # Only admin-approved entries are ever public -- this is the registry
    # any family can submit into via POST /submit, so anything pending or
    # rejected must never reach this endpoint.
    query = select(Person).where(Person.review_status == ReviewStatus.approved)
    if status:
        query = query.where(Person.status == status)
    persons = session.exec(query.order_by(Person.is_primary_target.desc(), Person.name)).all()
    return [_public_person(p) for p in persons]


@router.get("/primary-targets")
def list_primary_targets(session: Session = Depends(get_session)):
    query = select(Person).where(
        Person.is_primary_target == True,  # noqa: E712
        Person.review_status == ReviewStatus.approved,
    )
    persons = session.exec(query.order_by(Person.name)).all()
    return [_public_person(p) for p in persons]


@router.post("/submit")
def submit_person(payload: PersonSubmitIn, session: Session = Depends(get_session)):
    """Public: register a missing or deceased loved one, any nationality.
    Always starts pending -- never appears in the tables above until an
    admin reviews and approves it.
    """
    person = Person(
        **payload.model_dump(),
        is_primary_target=False,
        review_status=ReviewStatus.pending,
    )
    session.add(person)
    session.commit()
    session.refresh(person)
    return {
        "id": person.id,
        "status": "pending",
        "message": "Thank you. This entry is pending admin review before it appears in the public tables.",
    }
