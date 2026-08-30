from fastapi import APIRouter, Depends
from sqlmodel import Session, func, select

from ..database import get_session
from ..models import CrisisStats, Person, PersonStatus, ReviewStatus
from ..schemas import StatsOut

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("", response_model=StatsOut)
def get_stats(session: Session = Depends(get_session)):
    hub_missing = session.exec(
        select(func.count())
        .select_from(Person)
        .where(Person.status == PersonStatus.missing, Person.review_status == ReviewStatus.approved)
    ).one()
    hub_deceased = session.exec(
        select(func.count())
        .select_from(Person)
        .where(Person.status == PersonStatus.deceased, Person.review_status == ReviewStatus.approved)
    ).one()
    row = session.exec(select(CrisisStats)).first()

    nepal_missing = row.nepal_missing if row else 0
    tibet_missing = row.tibet_missing if row else 0
    nepal_dead = row.nepal_confirmed_dead if row else 0
    tibet_dead = row.tibet_confirmed_dead if row else 0

    return StatsOut(
        # The headline "Still Missing" / "Confirmed Deceased" tolls are the
        # official aggregate across ALL nationalities (Nepal + Tibet
        # combined), not a count of named entries on this site -- most
        # people in the official toll will never have an individual Person
        # record here.
        still_missing_count=nepal_missing + tibet_missing,
        confirmed_deceased_count=nepal_dead + tibet_dead,
        hub_registered_missing_count=hub_missing,
        hub_registered_deceased_count=hub_deceased,
        nepal_confirmed_dead=nepal_dead,
        nepal_missing=nepal_missing,
        tibet_confirmed_dead=tibet_dead,
        tibet_missing=tibet_missing,
        total_rescued=row.total_rescued if row else 0,
        total_group_members=row.total_group_members if row else 0,
        official_rescued_count=row.official_rescued_count if row else 0,
        note=row.note if row else None,
    )
