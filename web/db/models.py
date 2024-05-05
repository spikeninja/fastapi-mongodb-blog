from typing import List
from datetime import datetime

import pymongo
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

    model_config = {
        'indexes': lambda: [
            pymongo.IndexModel(
                [(+PostModel.text, pymongo.TEXT), (+PostModel.title, pymongo.TEXT)]
            )
        ]
    }


class CommentModel(Model):
    post_id: ObjectId
    text: str
    author: UserModel = Reference()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        'indexes': lambda: [
            pymongo.IndexModel(
                [(+CommentModel.text, pymongo.TEXT)]
            )
        ]
    }


class LikeModel(Model):
    user_id: ObjectId
    post_id: ObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
