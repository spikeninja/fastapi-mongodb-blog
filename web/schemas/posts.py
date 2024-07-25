from datetime import datetime
from typing import List, Literal

from odmantic import ObjectId
from pydantic import BaseModel
from schemas.user import UserPublic
from schemas.mixins import FilterBase, SorterBase


class PostCreateRequest(BaseModel):
    text: str
    title: str
    tags: List[str]


class PostUpdateRequest(BaseModel):
    text: str | None = None
    title: str | None = None
    tags: List[str] | None = None


class PostPublicSchema(BaseModel):
    id: ObjectId
    text: str
    title: str
    tags: List[str]
    author: UserPublic
    created_at: datetime
    updated_at: datetime


class PostFilter(FilterBase):
    field: Literal["id"]


class PostSorter(SorterBase):
    field: Literal["id", "created_at"]


class PostSearchSchema(BaseModel):
    limit: int
    offset: int
    q: str | None = None
    filters: list[PostFilter] | None = None
    sorters: list[PostSorter] | None = None
