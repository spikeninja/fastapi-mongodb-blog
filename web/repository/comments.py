from typing import List, Tuple
from datetime import datetime

from odmantic import ObjectId
from odmantic.query import QueryExpression

from repository.base import BaseRepository
from db.models import CommentModel, UserModel
from repository.utils import apply_sorters, apply_filters


class CommentsRepository(BaseRepository):

    async def get_all(
        self,
        limit: int | None,
        offset: int | None,
        filters: list[dict] | None,
        sorters: list[dict] | None,
        q: str | None = None,
        custom_filters: list[dict] | None = None,
    ) -> Tuple[List[CommentModel], int]:
        """"""

        filters_query = await apply_filters(
            filters=filters,
            model=CommentModel,
        )
        sorters_query = await apply_sorters(
            sorters=sorters,
            model=CommentModel,
        )

        if q:
            filters_query &= QueryExpression({
                "$text": {"$search": q}
            })

        if custom_filters:
            for _filter in custom_filters:
                filters_query &= QueryExpression(_filter)

        comments = await self.database.find(
            CommentModel,
            filters_query,
            limit=limit,
            skip=offset or 0,
            sort=sorters_query,
        )
        count = await self.database.count(
            CommentModel,
            filters_query
        )

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
