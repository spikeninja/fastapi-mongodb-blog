from typing import Literal
from datetime import datetime

from odmantic import ObjectId
from pydantic import BaseModel

from schemas.user import UserPublic
from schemas.mixins import FilterBase, SorterBase


class CommentCreateRequest(BaseModel):
    text: str


class CommentUpdateRequest(BaseModel):
    text: str


class CommentPublicSchema(BaseModel):
    id: ObjectId
    text: str
    author: UserPublic
    created_at: datetime


class CommentFilter(FilterBase):
    field: Literal["id"]


class CommentSorter(SorterBase):
    field: Literal["id", "created_at"]


class CommentSearchSchema(BaseModel):
    limit: int
    offset: int
    q: str | None = None
    filters: list[CommentFilter] | None = None
    sorters: list[CommentSorter] | None = None
