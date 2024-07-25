from fastapi import APIRouter, Depends, HTTPException, status

from odmantic import ObjectId
from db.models import UserModel
from ext.fastapi_ext import cbv
from schemas.mixins import ResponseItems
from api.dependencies import get_current_user, get_comments_repository, CommentsRepository
from schemas.comments import CommentUpdateRequest, CommentPublicSchema, CommentSearchSchema

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
        post_id: str | None = None,
    ):
        """"""

        comments, count = await self.comments_repo.get_all(
            q=q,
            limit=limit,
            offset=offset,
            filters=[{
                "field": "post_id",
                "operation": "eq",
                "value": ObjectId(post_id),
            }] if post_id else None,
            sorters=[{"order": "desc", "field": "created_at"}],
        )

        return {"items": comments, "count": count}

    @router.post(
        "/search",
        response_model=ResponseItems[CommentPublicSchema]
    )
    async def search(self, request: CommentSearchSchema):
        """"""

        raw_request = request.model_dump()

        comments, count = await self.comments_repo.get_all(
            q=request.q,
            limit=request.limit,
            offset=request.offset,
            sorters=raw_request['sorters'],
            filters=raw_request['filters'],
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

        comment_db = await self.comments_repo.get_by_id(_id=_id)
        if not comment_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id={_id} is not found"
            )

        if comment_db.author.id != self.current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have no access to this resourse"
            )

        await self.comments_repo.delete(_id=_id)

        return comment_db
