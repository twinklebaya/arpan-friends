"""Seed placeholder data so the app is fully navigable out of the box.

Every human-readable field below is a clearly-labeled placeholder. Replace
via the admin API (or directly in the DB) with verified details before this
goes live -- do not ship these placeholder strings to a public audience.
"""

from sqlmodel import Session, select

from .database import engine
from .models import CrisisStats, Person

PRIMARY_TARGETS = [
    {"name": "Arpan Mithalal Kothari", "age": 40},
    {"name": "Karan Bhardwaj", "age": 40},
    {"name": "Bhavinkumar Rajnikant Raval", "age": 41},
    {"name": "PLACEHOLDER: 4th traveler full name", "age": None},
    {"name": "PLACEHOLDER: 5th traveler full name", "age": None},
    {"name": "PLACEHOLDER: 6th traveler full name", "age": None},
]


def seed_if_empty() -> None:
    with Session(engine) as session:
        existing = session.exec(select(Person)).first()
        if existing:
            return

        for entry in PRIMARY_TARGETS:
            session.add(
                Person(
                    name=entry["name"],
                    age=entry["age"],
                    is_primary_target=True,
                    status="missing",
                    last_seen_location="Gyirong border crossing, Rasuwa district (Nepal-Tibet border) -- CONFIRM exact last-seen point",
                    physical_markers="PLACEHOLDER: add verified distinct physical markers (clothing, build, tattoos, etc.)",
                    photo_url=None,  # add a verified real photo URL per person before launch
                )
            )

        session.add(CrisisStats(total_group_members=len(PRIMARY_TARGETS), official_rescued_count=0,
                                 note="PLACEHOLDER stats -- replace with official counts"))
        session.commit()
