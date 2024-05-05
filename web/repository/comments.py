from typing import List, Tuple
from datetime import datetime

from odmantic import ObjectId, query

from repository.base import BaseRepository
from db.models import CommentModel, UserModel


class CommentsRepository(BaseRepository):

    async def get_all(
        self, limit: int | None, offset: int | None, filters: dict | None, q: str | None = None
    ) -> Tuple[List[CommentModel], int]:
        """"""

        queries = []
        if filters:
            queries = [getattr(CommentModel, k) == v for k, v in filters.items()]

        if q:
            # queries.append(CommentModel.find({"$text": {"$search": q}}))
            pass

        comments = await self.database.find(
            CommentModel,
            queries,
            limit=limit,
            skip=offset,
            sort=query.desc(CommentModel.created_at),
        )
        count = await self.database.count(CommentModel, queries)

        return comments, count

    async def get_by_id(self, _id: str) -> CommentModel | None:
        """"""
        return await self.database.find_one(CommentModel, CommentModel.id == ObjectId(_id))

    async def get_by_field(self, field: str, value: any) -> CommentModel | None:
        """"""

        return await self.database.find_one(CommentModel, getattr(CommentModel, field) == value)

    async def create(
        self,
        text: str,
        post_id: str,
        author_id: str,
    ) -> CommentModel:
        """"""

        user = await self.database.find_one(UserModel, UserModel.id == ObjectId(author_id))

        comment = CommentModel(
            text=text,
            author=user,
            post_id=ObjectId(post_id),
        )

        return await self.database.save(comment)

    async def update(self, _id: str, values: dict) -> CommentModel:
        """"""

        comment = await self.get_by_id(_id=_id)

        now_ = datetime.utcnow()
        comment.model_update({**values, "updated_at": now_})

        return await self.database.save(comment)

    async def delete(self, _id: str):
        """"""

        comment = await self.get_by_id(_id=_id)

        await self.database.delete(comment)
