import redis.asyncio as redis
from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient
from dependency_injector.providers import ThreadSafeSingleton

from core.config import settings


def get_redis() -> redis:
    return redis.from_url("redis://redis:6379/4")


def get_db() -> AIOEngine:
    """Connects to MongoDB instance and returns current DB"""

    client = AsyncIOMotorClient(settings.mongodb_url)
    return AIOEngine(client=client, database=settings.mongodb_database)


DatabaseProvider = ThreadSafeSingleton(get_db)
