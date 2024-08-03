from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query

from odmantic import ObjectId
from ext.fastapi_ext import cbv
from db.models import UserModel
from schemas.mixins import ResponseItems
from schemas.comments import CommentCreateRequest, CommentPublicSchema
from schemas.posts import PostCreateRequest, PostUpdateRequest, PostPublicSchema, PostSearchSchema
from api.dependencies import get_current_user, get_posts_repository, PostsRepository, CommentsRepository, get_comments_repository

router = APIRouter()


@cbv(router)
class PostsAPI:

    current_user: UserModel = Depends(get_current_user)
    posts_repo: PostsRepository = Depends(get_posts_repository)
    comments_repo: CommentsRepository = Depends(get_comments_repository)

    @router.get("/", response_model=ResponseItems[PostPublicSchema])
    async def get_all(
        self,
        q: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        author_id: str | None = None,
        tags: List[str] = Query(None, alias="tags"),
    ):
        """"""

        custom_filters = []

        if q:
            custom_filters.append({"$text": {"$search": q}})

        if tags:
            custom_filters.append({"tags": {"$all": tags}})

        posts, count = await self.posts_repo.get_all(
            limit=limit,
            offset=offset,
            filters=[{
                "field": "author",
                "operation": "eq",
                "val": ObjectId(author_id),
            }] if author_id else None,
            custom_filters=custom_filters,
            sorters=[{"field": "created_at", "order": "desc"}],
        )

        return {"items": posts, "count": count}

    @router.post("/search", response_model=ResponseItems[PostPublicSchema])
    async def search(self, request: PostSearchSchema):
        """"""

        raw_request = request.model_dump()

        custom_filters = []
        if request.q:
            custom_filters.append({"$text": {"$search": request.q}})

        posts, count = await self.posts_repo.get_all(
            limit=request.limit,
            offset=request.offset,
            sorters=raw_request['sorters'],
            filters=raw_request['filters'],
            custom_filters=custom_filters,
        )

        return {"items": posts, "count": count}

    @router.get("/{_id}", response_model=PostPublicSchema)
    async def get_by_id(self, _id: str):
        """"""

        post_db = await self.posts_repo.get_by_id(_id=_id)
        if not post_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id={_id} is not found"
            )

        return post_db

    @router.post("/", response_model=PostPublicSchema)
    async def create_post(self, request: PostCreateRequest):
        """"""

        return await self.posts_repo.create(
            tags=request.tags,
            text=request.text,
            title=request.title,
            author_id=self.current_user.id,
        )

    @router.patch("/{_id}", response_model=PostPublicSchema)
    async def update(self, _id: str, request: PostUpdateRequest):
        """"""

        return await self.posts_repo.update(_id=_id, values=request.model_dump(exclude_unset=True))

    @router.delete("/{_id}", response_model=PostPublicSchema)
    async def delete(self, _id: str):
        """"""

        post_db = await self.posts_repo.get_by_id(_id=_id)
        if not post_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id={_id} is not found"
            )

        if post_db.author.id != self.current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have no access to this resourse"
            )

        await self.posts_repo.delete(_id=_id)

        return post_db

    @router.post("/{_id}/comments", response_model=CommentPublicSchema)
    async def create_comment(self, _id: str, request: CommentCreateRequest):
        """"""

        return await self.comments_repo.create(
            post_id=_id,
            text=request.text,
            author_id=self.current_user.id,
        )
