from fastapi import APIRouter

from . import well_known, nodeinfo, box, actors

router = APIRouter()
router.include_router(well_known.router)
router.include_router(nodeinfo.router)
router.include_router(box.router)
router.include_router(actors.router)
