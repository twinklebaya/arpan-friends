"""Shared logic for turning a raw pasted excerpt into a pending
SourceUpdate row. Used by both the full admin API and the narrower
/api/ingest endpoint meant for external automation (e.g. a scheduled
ChatGPT/Claude task watching for news).

Whichever caller uses this, the result always lands as `pending` --
nothing here ever publishes to a feed or changes a person's status
directly. That only happens when a human approves it via the admin
review queue.
"""

from sqlmodel import Session, select

from ..models import Person, SourceType, SourceUpdate
from ..schemas import SourceUpdateIn
from .openrouter import classify_source_update


async def create_pending_source_update(payload: SourceUpdateIn, session: Session) -> SourceUpdate:
    target_names = session.exec(
        select(Person.name).where(Person.is_primary_target == True)  # noqa: E712
    ).all()

    ai_result = await classify_source_update(
        payload.raw_text, payload.source_name, payload.source_type.value, list(target_names)
    )

    matched_person_id = None
    if ai_result.get("person_match_name"):
        matched = session.exec(
            select(Person).where(Person.name == ai_result["person_match_name"])
        ).first()
        if matched:
            matched_person_id = matched.id

    status_suggestion = ai_result.get("status_suggestion")
    if payload.source_type == SourceType.social_media and status_suggestion == "deceased":
        # Hard backend guard: never let a social-media post drive a deceased
        # determination, even if the model didn't follow the prompt rule.
        status_suggestion = None

    update = SourceUpdate(
        raw_text=payload.raw_text,
        source_name=payload.source_name,
        source_url=payload.source_url,
        source_type=payload.source_type,
        feed_type_suggestion=ai_result.get("feed_type") or payload.feed_type_hint,
        ai_summary=ai_result.get("summary"),
        ai_person_match_id=matched_person_id,
        ai_status_suggestion=status_suggestion,
        ai_stats_suggestion=ai_result.get("stats_note"),
        ai_error=ai_result.get("ai_error"),
    )
    session.add(update)
    session.commit()
    session.refresh(update)
    return update
