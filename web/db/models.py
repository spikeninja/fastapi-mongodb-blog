from typing import List
from datetime import datetime

from odmantic import Field, Model, Reference, ObjectId


class UserModel(Model):
    name: str
    email: str
    hashed_password: str
    email_verified: bool
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PostModel(Model):
    text: str
    title: str
    tags: List[str]
    author: UserModel = Reference()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CommentModel(Model):
    text: str
    post_id: ObjectId
    author: UserModel = Reference()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class LikeModel(Model):
    user_id: ObjectId
    post_id: ObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
