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
    is_primary_target: bool = False  # the 6 Kailash Journeys individuals
    status: PersonStatus = PersonStatus.missing

    last_seen_location: str = ""
    found_location: Optional[str] = None
    physical_markers: str = ""

    photo_url: Optional[str] = None  # only ever shown while status == missing

    # Populated only when a deceased-status SourceUpdate is admin-approved.
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    confirmed_at: Optional[datetime] = None

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
    """Single-row table of group-wide tallies, editable by admins or via an
    approved SourceUpdate. Not derived from Person counts because these
    numbers (e.g. total group size, official rescued count) come from
    authorities and may not map 1:1 to individually-tracked Person rows.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    total_group_members: int = 0
    official_rescued_count: int = 0
    note: Optional[str] = None
    updated_at: datetime = Field(default_factory=utcnow)
