from fastapi import APIRouter, Depends
from sqlmodel import Session, func, select

from ..database import get_session
from ..models import CrisisStats, Person, PersonStatus
from ..schemas import StatsOut

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("", response_model=StatsOut)
def get_stats(session: Session = Depends(get_session)):
    still_missing = session.exec(
        select(func.count()).select_from(Person).where(Person.status == PersonStatus.missing)
    ).one()
    deceased = session.exec(
        select(func.count()).select_from(Person).where(Person.status == PersonStatus.deceased)
    ).one()
    row = session.exec(select(CrisisStats)).first()

    return StatsOut(
        still_missing_count=still_missing,
        confirmed_deceased_count=deceased,
        total_group_members=row.total_group_members if row else 0,
        official_rescued_count=row.official_rescued_count if row else 0,
        note=row.note if row else None,
    )
