from fastapi import APIRouter

from delvify.api.v1 import index, users

ms_router = APIRouter(prefix="/api/v1", tags=["v1"])

ms_router.include_router(index.endpoint, prefix="/index", tags=["index"])
ms_router.include_router(users.endpoint, prefix="/users", tags=["users"])
