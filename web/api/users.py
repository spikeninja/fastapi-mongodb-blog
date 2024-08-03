from fastapi import APIRouter, Depends

from db.models import UserModel
from ext.fastapi_ext import cbv
from schemas.user import UserPublic
from repository.users import UserRepository
from api.dependencies import get_current_user, get_user_repository


router = APIRouter()


@cbv(router)
class UsersRouter:

    users_repo: UserRepository = Depends(get_user_repository)

    @router.get("/me", response_model=UserPublic)
    async def get_me(self, current_user: UserModel = Depends(get_current_user)):
        """"""

        return current_user

    @router.get("/{user_id}", response_model=UserPublic)
    async def get_by_id(self, user_id: str):
        """"""

        return await self.users_repo.get_by_id(user_id=user_id)
