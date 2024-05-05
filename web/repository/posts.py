from datetime import datetime
from typing import List, Tuple

from odmantic import ObjectId
from odmantic.query import QueryExpression, desc

from repository.base import BaseRepository
from db.models import PostModel, LikeModel, UserModel


class PostsRepository(BaseRepository):

    async def get_all(
        self,
        limit: int | None,
        offset: int | None,
        filters: dict | None,
        q: str | None = None,
    ) -> Tuple[List[PostModel], int]:
        """"""

        query = QueryExpression()
        if filters:
            for key, value in filters.items():
                query &= (getattr(PostModel, key) == value)

        if q:
            query &= QueryExpression({"$text": {"$search": q}})

        posts = await self.database.find(
            PostModel,
            query,
            limit=limit,
            skip=offset or 0,
            sort=desc(PostModel.created_at),
        )

        count = await self.database.count(PostModel, query)

        return posts, count

    async def get_by_id(self, _id: str) -> PostModel | None:
        """"""
        return await self.database.find_one(PostModel, PostModel.id == ObjectId(_id))

    async def get_by_field(self, field: str, value: any) -> PostModel | None:
        """"""

        return await self.database.find_one(PostModel, getattr(PostModel, field) == value)

    async def create(
        self,
        text: str,
        title: str,
        author_id: str,
        tags: List[str],
    ) -> PostModel:
        """"""

        author = await self.database.find_one(UserModel, UserModel.id == ObjectId(author_id))

        post = PostModel(
            tags=tags,
            text=text,
            title=title,
            author=author,
        )

        return await self.database.save(post)

    async def update(self, _id: str, values: dict) -> PostModel:
        """"""

        post = await self.get_by_id(_id=_id)

        now_ = datetime.utcnow()
        post.model_update({**values, "updated_at": now_})

        return await self.database.save(post)

    async def delete(self, _id: str):
        """"""
        post = await self.get_by_id(_id=_id)

        await self.database.delete(post)

    async def like(self, post_id: str, author_id: str):
        """"""

    async def unlike(self, post_id: str, author_id: str):
        """"""
