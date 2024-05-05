from fastapi import APIRouter, Depends

from db.models import UserModel
from ext.fastapi_ext import cbv
from schemas.user import UserPublic
from api.dependencies import get_current_user


router = APIRouter()


@cbv(router)
class UsersRouter:

    @router.get("/me", response_model=UserPublic)
    async def get_me(self, current_user: UserModel = Depends(get_current_user)):
        """"""

        return current_user
