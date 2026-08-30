from typing import Literal, Optional

from pydantic import BaseModel, Field

from .models import FeedType, PersonStatus, SourceType


class StatsOut(BaseModel):
    still_missing_count: int
    confirmed_deceased_count: int
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


class PersonUpdateIn(BaseModel):
    status: Optional[PersonStatus] = None
    found_location: Optional[str] = None
    physical_markers: Optional[str] = None
    last_seen_location: Optional[str] = None
    source_name: Optional[str] = None
    source_url: Optional[str] = None


class StatsUpdateIn(BaseModel):
    total_group_members: Optional[int] = None
    official_rescued_count: Optional[int] = None
    note: Optional[str] = None
