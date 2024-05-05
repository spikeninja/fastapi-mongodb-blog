from datetime import datetime

from odmantic import ObjectId
from pydantic import BaseModel

from schemas.user import UserPublic


class CommentCreateRequest(BaseModel):
    text: str


class CommentUpdateRequest(BaseModel):
    text: str


class CommentPublicSchema(BaseModel):
    id: ObjectId
    text: str
    author: UserPublic
    created_at: datetime
