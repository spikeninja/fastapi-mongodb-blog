from fastapi import APIRouter, Depends, HTTPException, status

from odmantic import ObjectId
from ext.fastapi_ext import cbv
from db.models import UserModel
from schemas.mixins import ResponseItems
from schemas.comments import CommentCreateRequest, CommentPublicSchema
from schemas.posts import PostCreateRequest, PostUpdateRequest, PostPublicSchema
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
    ):
        """"""

        posts, count = await self.posts_repo.get_all(
            q=q,
            limit=limit,
            offset=offset,
            filters={"author_id": ObjectId(author_id)} if author_id else None
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
    async def create(self, request: PostCreateRequest):
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
    async def create(self, _id: str, request: CommentCreateRequest):
        """"""

        return await self.comments_repo.create(
            post_id=_id,
            text=request.text,
            author_id=self.current_user.id,
        )
