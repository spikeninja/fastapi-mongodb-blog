import datetime

import bcrypt

from jose import jwt, JWTError
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.config import settings


async def hash_password(password: str) -> str:
    """Async wrapper for bcrypt operation"""

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


async def verify_password(password: str, hashed: str) -> bool:
    """"""

    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


async def create_access_token(data: dict) -> str:
    """"""

    to_encode = data.copy()

    to_encode.update({
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.access_token_expire_minutes)
    })

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


async def decode_access_token(token: str):
    """"""
    try:
        decoded_jwt = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

    except jwt.JWSError:

        return None

    return decoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        try:
            credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        except HTTPException as e:
            raise HTTPException(
                detail=e.detail,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        exp = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid auth token"
        )

        if credentials:
            try:
                token = await decode_access_token(credentials.credentials)
            except JWTError as _:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid auth token"
                )

            if token is None:
                raise exp

            return credentials.credentials

        else:
            raise exp
