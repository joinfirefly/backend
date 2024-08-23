from robyn import SubRouter

from . import well_known, nodeinfo, box, actors

router = SubRouter("Holo")
router.include_router(well_known.router)
router.include_router(nodeinfo.router)
router.include_router(box.router)
router.include_router(actors.router)
