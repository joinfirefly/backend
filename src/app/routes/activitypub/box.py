import logging
from typing import List
import json

import aiohttp
import aputils
from robyn import SubRouter, Request

from prisma.models import User
from Crypto.PublicKey import RSA

from ...utils import log
from ... import __version__

router = SubRouter("Holo")
logger, formatter = log.getLogger(__name__)
handler = logging.FileHandler('./.logs/{:%Y-%m-%d}.log'.format(log.logConfig.time))
handler.setFormatter(formatter)
logger.addHandler(handler)

@router.post("/inbox")
async def sharedInbox(request: Request):
    pass

@router.post("/users/{userid}/inbox")
async def inbox(request: Request, userid: str):
    pass