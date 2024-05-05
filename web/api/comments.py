from fastapi import APIRouter, Depends, HTTPException, status

from odmantic import ObjectId
from db.models import UserModel
from ext.fastapi_ext import cbv
from schemas.mixins import ResponseItems
from api.dependencies import get_current_user, get_comments_repository, CommentsRepository
from schemas.comments import CommentCreateRequest, CommentUpdateRequest, CommentPublicSchema

router = APIRouter()


@cbv(router)
class CommentsAPI:

    current_user: UserModel = Depends(get_current_user)
    comments_repo: CommentsRepository = Depends(get_comments_repository)

    @router.get("/", response_model=ResponseItems[CommentPublicSchema])
    async def get_all(
        self,
        q: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        author_id: str | None = None,
    ):
        """"""

        comments, count = await self.comments_repo.get_all(
            q=q,
            limit=limit,
            offset=offset,
            filters={"author_id": ObjectId(author_id)} if author_id else None
        )

        return {"items": comments, "count": count}

    @router.get("/{_id}", response_model=CommentPublicSchema)
    async def get_by_id(self, _id: str):
        """"""

        comment_db = await self.comments_repo.get_by_id(_id=_id)
        if not comment_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id={_id} is not found"
            )

        return comment_db

    @router.patch("/{_id}", response_model=CommentPublicSchema)
    async def update(self, _id: str, request: CommentUpdateRequest):
        """"""

        return await self.comments_repo.update(_id=_id, values=request.model_dump(exclude_unset=True))

    @router.delete("/{_id}", response_model=CommentPublicSchema)
    async def delete(self, _id: str):
        """"""

        post_db = await self.comments_repo.get_by_id(_id=_id)
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

        await self.comments_repo.delete(_id=_id)

        return post_db
