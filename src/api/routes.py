from fastapi import APIRouter

from .api_v1.user import user
from .api_v1.auth import auth
from .api_v1.jogging import jogging

router = APIRouter()
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(jogging.router)
