import string
import random
from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.database import DatabaseProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    """"""
    database = DatabaseProvider()
    yield
    database.client.close()


def generate_class_code(code_length=6):
    characters = string.ascii_letters + string.digits
    result = ''.join(random.choice(characters) for _ in range(code_length))
    return result
