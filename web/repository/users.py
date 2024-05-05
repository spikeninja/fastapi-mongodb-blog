from datetime import datetime

from odmantic import ObjectId

from db.models import UserModel
from schemas.user import UserCreate
from core.security import hash_password
from repository.base import BaseRepository


class UserRepository(BaseRepository):

    async def get_by_id(self, user_id: str) -> UserModel | None:
        """"""

        return await self.database.find_one(UserModel, UserModel.id == ObjectId(user_id))

    async def get_by_field(self, field: str, value: any) -> UserModel | None:
        """"""

        return await self.database.find_one(UserModel, getattr(UserModel, field) == value)

    async def create(self, user: UserCreate) -> UserModel:
        """"""

        hashed_password = await hash_password(password=user.password)

        user = UserModel(
            name=user.name,
            email=user.email,
            email_verified=False,
            hashed_password=hashed_password,
        )

        return await self.database.save(user)

    async def update(self, _id: str, values: dict) -> UserModel:
        """"""

        user = await self.get_by_id(user_id=_id)

        now_ = datetime.utcnow()
        user.model_update({**values, "updated_at": now_})

        return await self.database.save(user)

    async def decrease_credits(self, _id: str, number: int) -> UserModel:
        """"""

        user = await self.get_by_id(user_id=_id)
        user.credits -= number

        return await self.database.save(user)
