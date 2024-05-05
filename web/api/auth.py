from fastapi import APIRouter, Depends, HTTPException, status

from ext.fastapi_ext import cbv
from schemas.user import UserCreate
from repository.users import UserRepository
from api.dependencies import get_user_repository
from schemas.auth import LoginRequest, AuthResponse
from core.security import verify_password, create_access_token


router = APIRouter()


@cbv(router)
class AuthRouter:

    users_repo: UserRepository = Depends(get_user_repository)

    @router.post("/login", response_model=AuthResponse)
    async def auth(self, login: LoginRequest):
        """"""

        db_user = await self.users_repo.get_by_field(field='email', value=login.email)

        if not db_user:
            raise HTTPException(
                detail="User with such email does not exist",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        password_verified = await verify_password(login.password, db_user.hashed_password)

        if not password_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect credentials"
            )

        token = await create_access_token({'sub': str(db_user.id)})

        return {'access_token': token, 'user': db_user}

    @router.post("/register", response_model=AuthResponse)
    async def register(self, user: UserCreate):
        """"""

        db_user = await self.users_repo.get_by_field(field='email', value=user.email)

        if db_user:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )

        user = await self.users_repo.create(user=user)
        token = await create_access_token({'sub': str(user.id)})

        return {'access_token': token, 'user': user}
