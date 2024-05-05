from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils import lifespan
from api import auth, posts, users, comments


def application_factory(openapi_url: str = "/openapi.json") -> FastAPI:
    """"""

    app = FastAPI(lifespan=lifespan, openapi_url=openapi_url)

    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(users.router, prefix="/api/users", tags=["users"])
    app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
    app.include_router(comments.router, prefix="/api/comments", tags=["comments"])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    return app
