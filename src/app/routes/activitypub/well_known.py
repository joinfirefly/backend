import logging

from fastapi import APIRouter, Request
from robyn import SubRouter, Response, jsonify


from prisma.models import BEConfig, User
from ...utils.responses import XMLResponse

router = SubRouter("Holo", prefix="/.well-known")

logger: logging.Logger = None


@router.get("/nodeinfo")
async def nodeinfo(request: Request):
    instance = await BEConfig.prisma().find_first(where={"id": "hol0"})
    return {
        "links": [
            {
                "rel": "http://nodeinfo.diaspora.software/ns/schema/2.1",
                "href": f"https://{instance.host}/nodeinfo/2.1",
            },
            {
                "rel": "http://nodeinfo.diaspora.software/ns/schema/2.0",
                "href": f"https://{instance.host}/nodeinfo/2.0",
            },
        ]
    }


@router.get("/webfinger")
async def webfinger(resource: str):
    instance = await BEConfig.prisma().find_first(where={"id": "hol0"})
    if resource.startswith("acct:"):
        acct = resource.split("acct:")[1].split("@")
        try:
            if acct[1] != instance.host:
                return Response(status_code=404)
        except IndexError:
            return Response(status_code=400)
    else:
        return Response(status_code=400)
    user = await User.prisma().find_first(
        where={"normalizedUserName": acct[0].lower(), "host": None}
    )
    if user is None:
        return Response(status_code=404)
    return {
        "subject": f"acct:{acct[0]}@{acct[1]}",
        "links": [
            {
                "rel": "http://webfinger.net/rel/profile-page",
                "type": "text/html",
                "href": f"https://{instance.host}/@{user.username}",
            },
            {
                "rel": "self",
                "type": "application/activity+json",
                "href": f"https://{instance.host}/users/{user.id}",
            },
        ],
    }


@router.get("/host-meta")
@router.get("/host-meta.json")
async def host_meta(request: Request):
    instance = await BEConfig.prisma().find_first(where={"id": "hol0"})
    if request.url.path == "/.well-known/host-meta":
        hm = (
            f"""<?xml version="1.0"?>
        <XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">
            <Link rel="lrdd" type="application/xrd+xml" template="https://{instance.host}/.well-known/webfinger"""
            + """?resource={uri}" />
        </XRD>"""
        )
        return XMLResponse(xml_body=hm)
    elif request.url.path == "/.well-known/host-meta.json":
        return {
            "links": [
                {
                    "rel": "lrdd",
                    "type": "application/jrd+json",
                    "template": f"https://{instance.host}/.well-known/webfinger?resource="
                    + "{uri}",
                }
            ]
        }
