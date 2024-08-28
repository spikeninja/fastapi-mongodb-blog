from enum import Enum
from datetime import datetime, timedelta

from redis.asyncio import Redis as AsyncRedis

from core.config import settings


class TwoFAStates(Enum):
    S1 = "S_1"
    S2 = "S_2"


class TwoFAField(Enum):
    code = 'code'
    email = 'email'
    attempts = 'attempts'
    two_fa_state = 'two_fa_state'
    two_fa_last_used = 'two_fa_last_used'
    two_fa_start_time = 'two_fa_start_time'


class TwoFA:

    def __init__(self, user_id: str):
        self.name = f'user_id:{user_id}'
        self.rclient = AsyncRedis.from_url(
            settings.two_fa_redis,
            decode_responses=True,
        )

    # HELPERS
    async def get_current_state(self,) -> str | None:
        """"""
        return await self.rclient.hget(
            name=self.name,
            key='two_fa_state'
        )

    async def two_fa_needed(self) -> bool:
        """"""
        last_time_raw = await self.rclient.hget(
            name=self.name,
            key=TwoFAField.two_fa_last_used.value,
        )

        if not last_time_raw:
            return True

        # todo: last_time = arrow.get(last_time_raw)
        last_time = datetime.utcnow()

        return last_time + timedelta(minutes=settings.two_fa_code_lifetime) < datetime.utcnow()

    async def set_state(self, state: str):
        """"""

        await self.rclient.hset(
            name=self.name,
            key='state',
            value=state,
        )

    async def is_code_valid(self, code: str) -> bool:
        """"""

        valid_code = await self.rclient.hget(name=self.name, key='code')

        return code == valid_code

    async def increase_attempts(self):
        """"""

        current_attempts = await self.rclient.hget(
            name=self.name,
            key='attempts',
        )

        await self.rclient.hset(
            name=self.name,
            key='attempts',
            value=int(current_attempts) + 1
        )

    # TWO_FA Processes
    async def initialize_process(self, email: str):
        await self.rclient.hset(
            name=self.name,
            mapping={
                "email": email,
                "two_fa_state": TwoFAStates.S1.value,
            },
        )

    async def set_code(self, code: str):
        await self.rclient.hset(
            name=self.name,
            mapping={
                "code": code,
                "attempts": 0,
                "two_fa_state": TwoFAStates.S2.value,
                "two_fa_start_time": datetime.utcnow(),
            },
        )

    async def end_two_fa_process(self):
        """"""

        await self.rclient.hdel(
            self.name,
            *['email', 'code', 'two_fa_start_time', 'two_fa_state']
        )

        await self.rclient.hset(
            name=self.name,
            mapping={
                TwoFAField.two_fa_last_used.value: datetime.utcnow()
            }
        )
