from datetime import datetime

from pydantic import BaseModel

from schemas.user import UserPublic


class CommentCreateRequest(BaseModel):
    text: str


class CommentUpdateRequest(BaseModel):
    text: str


class CommentPublicSchema(BaseModel):
    text: str
    author: UserPublic
    created_at: datetime
