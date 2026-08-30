from typing import Literal, Optional

from pydantic import BaseModel, Field

from .models import FeedType, PersonStatus, SourceType


class StatsOut(BaseModel):
    still_missing_count: int
    confirmed_deceased_count: int

    nepal_confirmed_dead: int
    nepal_missing: int
    tibet_confirmed_dead: int
    tibet_missing: int
    total_rescued: int

    total_group_members: int
    official_rescued_count: int
    note: Optional[str] = None


class TipCreateResponse(BaseModel):
    id: int
    status: Literal["pending"] = "pending"
    message: str = "Thank you. Your submission is pending admin review before it appears publicly."


class ReviewAction(BaseModel):
    action: Literal["approve", "reject"]


class SourceUpdateIn(BaseModel):
    raw_text: str = Field(min_length=1)
    source_name: str = Field(min_length=1)
    source_url: Optional[str] = None
    source_type: SourceType = SourceType.other
    feed_type_hint: Optional[FeedType] = None


class PersonCreateIn(BaseModel):
    name: str = Field(min_length=1)
    age: Optional[int] = None
    is_primary_target: bool = True
    status: PersonStatus = PersonStatus.missing
    last_seen_location: str = ""
    physical_markers: str = ""


class PersonSubmitIn(BaseModel):
    """Public submission: any family/friend registering a missing or
    deceased loved one, any nationality. Always starts pending review and
    is never a primary target -- those two things can only be set by an
    admin.
    """

    name: str = Field(min_length=1, max_length=200)
    age: Optional[int] = Field(default=None, ge=0, le=130)
    status: PersonStatus = PersonStatus.missing
    last_seen_location: str = Field(default="", max_length=1000)
    found_location: Optional[str] = Field(default=None, max_length=1000)
    physical_markers: str = Field(default="", max_length=1000)

    submitted_by_name: Optional[str] = Field(default=None, max_length=200)
    submitted_by_email: Optional[str] = Field(default=None, max_length=200)
    submitted_by_phone: Optional[str] = Field(default=None, max_length=50)


class PersonUpdateIn(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    status: Optional[PersonStatus] = None
    found_location: Optional[str] = None
    physical_markers: Optional[str] = None
    last_seen_location: Optional[str] = None
    source_name: Optional[str] = None
    source_url: Optional[str] = None


class StatsUpdateIn(BaseModel):
    nepal_confirmed_dead: Optional[int] = None
    nepal_missing: Optional[int] = None
    tibet_confirmed_dead: Optional[int] = None
    tibet_missing: Optional[int] = None
    total_rescued: Optional[int] = None
    total_group_members: Optional[int] = None
    official_rescued_count: Optional[int] = None
    note: Optional[str] = None
