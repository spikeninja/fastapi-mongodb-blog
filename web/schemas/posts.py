from typing import List
from datetime import datetime

from pydantic import BaseModel
from schemas.user import UserPublic


class PostCreateRequest(BaseModel):
    text: str
    title: str
    tags: List[str]


class PostUpdateRequest(BaseModel):
    text: str | None = None
    title: str | None = None
    tags: List[str] | None = None


class PostPublicSchema(BaseModel):
    text: str
    title: str
    tags: List[str]
    author: UserPublic
    created_at: datetime
    updated_at: datetime
