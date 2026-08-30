from typing import Optional

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..database import get_session
from ..models import Person, PersonStatus

router = APIRouter(prefix="/api/persons", tags=["persons"])


def _public_person(p: Person) -> dict:
    """Serialize a Person, stripping photo_url whenever status != missing.

    This is the hard enforcement point for "never show a photo of the
    deceased" -- even if a photo_url were ever set on a deceased record by
    mistake, it will not leave this function.
    """
    data = {
        "id": p.id,
        "name": p.name,
        "age": p.age,
        "is_primary_target": p.is_primary_target,
        "status": p.status,
        "last_seen_location": p.last_seen_location,
        "physical_markers": p.physical_markers,
        "photo_url": p.photo_url if p.status == PersonStatus.missing else None,
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
    query = select(Person)
    if status:
        query = query.where(Person.status == status)
    persons = session.exec(query.order_by(Person.is_primary_target.desc(), Person.name)).all()
    return [_public_person(p) for p in persons]


@router.get("/primary-targets")
def list_primary_targets(session: Session = Depends(get_session)):
    query = select(Person).where(Person.is_primary_target == True)  # noqa: E712
    persons = session.exec(query.order_by(Person.name)).all()
    return [_public_person(p) for p in persons]
