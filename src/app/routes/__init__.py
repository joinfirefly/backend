from robyn import SubRouter

from . import activitypub, avatar

router = SubRouter("Holo")
router.include_router(activitypub.router)
router.include_router(avatar.router)