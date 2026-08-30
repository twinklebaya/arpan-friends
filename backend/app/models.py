from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.utcnow()


class PersonStatus(str, Enum):
    missing = "missing"
    deceased = "deceased"


class FeedType(str, Enum):
    general = "general"
    target = "target"


class ReviewStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class SourceType(str, Enum):
    official = "official"  # Nepalese/Indian/Australian government or embassy statement
    news_media = "news_media"  # established news wire/outlet
    family = "family"  # firsthand family account, e.g. location data, direct interview
    social_media = "social_media"  # X/Twitter etc. -- unverified, lower trust
    other = "other"


class Person(SQLModel, table=True):
    """A tracked individual.

    Safety rule: `photo_url` must only ever be read/rendered by the UI when
    status == missing. It is never populated or shown once status flips to
    deceased (enforced again on the frontend table components).
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None
    is_primary_target: bool = False  # the Kailash Journeys individuals (hero + target feed)
    status: PersonStatus = PersonStatus.missing

    # Entries created by admins/ingestion default to approved. Public
    # submissions (any family registering a missing/deceased loved one from
    # any nationality) start pending and only appear in the public tables
    # once an admin approves them -- same review-gate philosophy as tips.
    review_status: ReviewStatus = ReviewStatus.approved

    last_seen_location: str = ""
    found_location: Optional[str] = None
    physical_markers: str = ""

    photo_url: Optional[str] = None  # primary photo -- only ever shown while status == missing
    photo_urls: str = "[]"  # JSON-encoded list of additional photo URLs, same hide-if-deceased rule

    # Populated only when a deceased-status SourceUpdate is admin-approved.
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    confirmed_at: Optional[datetime] = None

    # Submitter contact info, for admin follow-up only -- never exposed via
    # any public endpoint.
    submitted_by_name: Optional[str] = None
    submitted_by_email: Optional[str] = None
    submitted_by_phone: Optional[str] = None

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class SourceUpdate(SQLModel, table=True):
    """Raw text pasted in from an official source (embassy, Nepalese
    authorities, verified news wire), run through OpenRouter for
    classification, and held for admin approval before anything goes live.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    raw_text: str
    source_name: str
    source_url: Optional[str] = None
    source_type: SourceType = SourceType.other

    feed_type_suggestion: Optional[FeedType] = None
    ai_summary: Optional[str] = None
    ai_person_match_id: Optional[int] = Field(default=None, foreign_key="person.id")
    ai_status_suggestion: Optional[PersonStatus] = None
    ai_stats_suggestion: Optional[str] = None  # free-text, e.g. rescued count note
    ai_error: Optional[str] = None

    review_status: ReviewStatus = ReviewStatus.pending
    reviewed_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=utcnow)


class FeedItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    feed_type: FeedType
    title: str
    body: str
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    source_type: SourceType = SourceType.other

    origin: str = "ingestion"  # "ingestion" | "tip"
    source_update_id: Optional[int] = Field(default=None, foreign_key="sourceupdate.id")
    tip_id: Optional[int] = Field(default=None, foreign_key="tip.id")

    published_at: datetime = Field(default_factory=utcnow)


class Tip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    message: str
    image_paths: str = "[]"  # JSON-encoded list of stored file paths

    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

    ai_spam_likelihood: Optional[float] = None  # 0-1
    ai_notes: Optional[str] = None

    status: ReviewStatus = ReviewStatus.pending
    created_at: datetime = Field(default_factory=utcnow)
    reviewed_at: Optional[datetime] = None


class CrisisStats(SQLModel, table=True):
    """Single-row table of two distinct kinds of tallies:

    1. Official disaster-wide toll (nepal_*/tibet_* fields) -- aggregate
       figures from government/news sources, covering everyone affected
       across all nationalities, not just people named on this site.
    2. Kailash Journeys group-specific tallies (total_group_members,
       official_rescued_count) -- kept separate because they come from
       authorities and don't map 1:1 to individually-tracked Person rows.

    The site's own "still missing" / "confirmed deceased" counters (shown
    alongside these) are computed live from the Person table instead, since
    that table is a growing, admin-moderated registry that any family can
    add their loved one to -- it's expected to diverge from the official
    toll rather than duplicate it.
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    nepal_confirmed_dead: int = 0
    nepal_missing: int = 0
    tibet_confirmed_dead: int = 0
    tibet_missing: int = 0
    total_rescued: int = 0

    total_group_members: int = 0
    official_rescued_count: int = 0

    note: Optional[str] = None
    updated_at: datetime = Field(default_factory=utcnow)
