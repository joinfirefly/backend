import logging

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse, Response

import config

router = APIRouter(
    prefix="/.well-known",
    include_in_schema=False
)

logger : logging.Logger = None

def graphene_on_load():
    pass

@router.get("/nodeinfo")
async def nodeinfo():
    return ORJSONResponse(
        {
            "links": [
                {
                    "rel": "http://nodeinfo.diaspora.software/ns/schema/2.1",
                    "href": f"https://{config.host}/nodeinfo/2.1"
                }
            ]
        }
    )

@router.get("/webfinger")
async def webfinger(resource: str):
    if not resource.startswith("acct:"):
        acct = resource.split("acct:")[1].split("@")
        if acct[1] != config.host:
            return Response(status_code=404)
    return ORJSONResponse(
        {
        "subject": "acct:example@example.com",
            "links": [
                {
                "rel": "http://webfinger.net/rel/profile-page",
                "type": "text/html",
                "href": f"https://{config.host}/@sonyakun"
                },
                {
                    "rel": "self",
                    "type": "application/activity+json",
                    "href": "https://example.com/actor"
                }
            ]
        }
    )

@router.get("/host-meta")
async def host_meta():
    hm = f"""<?xml version="1.0"?>
    <XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">
        <Link rel="lrdd" type="application/xrd+xml" template="https://{config.host}/.well-known/webfinger""" + """?resource={uri}" />
    </XRD>"""
    return Response(content=hm, media_type="application/xml")