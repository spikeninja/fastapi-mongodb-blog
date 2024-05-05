from odmantic import AIOEngine
from fastapi import HTTPException, Depends, status

from core.config import settings
from db.files import MinioProvider
from services.files import FilesService
from db.database import DatabaseProvider
from repository.users import UserRepository
from repository.posts import PostsRepository
from repository.comments import CommentsRepository
from core.security import decode_access_token, JWTBearer


def get_database() -> AIOEngine:
    return DatabaseProvider()


def get_file_service() -> FilesService:
    return FilesService(
        minio_client=MinioProvider(),
        bucket_name=settings.bucket_name,
    )


# REPOSITORIES STUFF
def get_user_repository() -> UserRepository:
    return UserRepository(database=get_database())


def get_posts_repository() -> PostsRepository:
    return PostsRepository(database=get_database())


def get_comments_repository() -> CommentsRepository:
    return CommentsRepository(database=get_database())


async def get_current_user(
    user_repo: UserRepository = Depends(get_user_repository),
    token: str = Depends(JWTBearer())
):
    """"""

    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials are not valid."
    )

    payload = await decode_access_token(token)

    if not payload:
        raise cred_exception

    user_id = payload.get("sub", None)

    if not user_id:
        raise cred_exception

    user = await user_repo.get_by_id(user_id=user_id)

    if not user:
        raise cred_exception

    return user
