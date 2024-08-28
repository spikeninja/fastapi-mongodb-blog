from fastapi import APIRouter, Depends, HTTPException, status

from db.models import UserModel
from ext.fastapi_ext import cbv
from repository.users import UserRepository
from core.security import verify_password, hash_password
from schemas.user import UserPublic, UserUpdate, PasswordUpdate
from api.dependencies import get_current_user, get_user_repository


router = APIRouter()


@cbv(router)
class UsersRouter:

    users_repo: UserRepository = Depends(get_user_repository)

    @router.get("/me", response_model=UserPublic)
    async def get_me(self, current_user: UserModel = Depends(get_current_user)):
        """"""

        return current_user

    @router.patch("/me", response_model=UserPublic)
    async def update_me(
        self,
        request: UserUpdate,
        current_user: UserModel = Depends(get_current_user),
    ):
        """"""

        await self.users_repo.update(
            _id=current_user.id,
            values=request.model_dump(exclude_unset=True)
        )

        return await self.users_repo.get_by_id(user_id=current_user.id)

    @router.post("/me/password")
    async def change_password(
        self,
        request: PasswordUpdate,
        current_user: UserModel = Depends(get_current_user),
    ):
        """"""

        password_correct = await verify_password(
            password=request.old_password,
            hashed=current_user.hashed_password,
        )

        if not password_correct:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect opration"
            )

        if request.new_password == request.old_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password should be different"
            )

        new_hashed = await hash_password(password=request.new_password)

        await self.users_repo.update(
            _id=current_user.id,
            values={
                "hashed_password": new_hashed,
            }
        )

        return await self.users_repo.get_by_id(user_id=current_user.id)

    @router.get("/{user_id}", response_model=UserPublic)
    async def get_by_id(self, user_id: str):
        """"""

        return await self.users_repo.get_by_id(user_id=user_id)
