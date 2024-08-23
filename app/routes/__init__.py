from fastapi import APIRouter

from . import activitypub, avatar

router = APIRouter()
router.include_router(activitypub.router)
router.include_router(avatar.router)