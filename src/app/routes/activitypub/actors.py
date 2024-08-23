import logging

from prisma.models import User
from robyn import SubRouter, Response, jsonify, Request

from prisma.models import BEConfig

router = SubRouter("Holo")
logger: logging.Logger = None


@router.get("/users/{userid}")
async def users(request: Request, userid: str):
    accept = request.headers.get("Accept", None).split(", ")
    if "application/activity+json" not in accept:
        return Response(status_code=400)
    user = await User.prisma().find_first(where={"id": userid, "host": None})
    instance = await BEConfig.prisma().find_first(where={"id": "hol0"})
    if user is None:
        return Response(status_code=404)
    actor = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
            {
                "Key": "sec:Key",
                "manuallyApprovesFollowers": "as:manuallyApprovesFollowers",
                "sensitive": "as:sensitive",
                "Hashtag": "as:Hashtag",
                "quoteUrl": "as:quoteUrl",
                "toot": "http://joinmastodon.org/ns#",
                "Emoji": "toot:Emoji",
                "featured": "toot:featured",
                "discoverable": "toot:discoverable",
                "schema": "http://schema.org#",
                "PropertyValue": "schema:PropertyValue",
                "value": "schema:value",
            },
        ],
        "id": f"https://{instance.host}/users/{user.id}",
        "type": "Person",
        "preferredUsername": user.username,
        "inbox": f"https://{instance.host}/users/{user.id}/inbox",
        "outbox": f"https://{instance.host}/users/{user.id}/outbox",
        "sharedInbox": f"https://{instance.host}/inbox",
        "endpoints": {"sharedInbox": f"https://{instance.host}/inbox"},
        "icon": {
            "type": "Image",
            "url": user.avatarUrl,
            "sensitive": False,
            "name": None,
        },
        "image": {
            "type": "Image",
            "url": user.bannerUrl,
            "sensitive": False,
            "name": None,
        },
        "publicKey": {
            "id": f"https://{instance.host}/users/{user.id}#main-key",
            "owner": f"https://{instance.host}/users/{user.id}",
            "publicKeyPem": user.publicKeyPem,
            "type": "Key",
        },
        "url": f"https://{instance.host}/@{user.username}",
    }
    if user.description:
        actor["summary"] = user.description
    if user.displayName:
        actor["name"] = user.displayName
    if user.avatarUrl:
        actor["icon"] = {
            "type": "Image",
            "url": user.avatarUrl,
            "sensitive": False,
            "name": None,
        }
    if user.bannerUrl:
        actor["image"] = {
            "type": "Image",
            "url": user.bannerUrl,
            "sensitive": False,
            "name": None,
        }
    return Response(jsonify(actor), headers={"Content-Type": "application/activity+json"})


"""
@router.post("/{userid}/inbox")
async def inbox(request: Request, userid: str):
    inbox_obj = await request.json()
    with open("note.json", "wb") as f:
        f.write(orjson.dumps(inbox_obj))
    with open("note_head.txt", "wb") as f:
        f.write(orjson.dumps(dict(request.headers)))
    accept = request.headers.get("Accept", None).split(", ")
    if "application/activity+json" not in accept:
        return Response(status_code=400)
    user = await User.prisma().find_first(where={"id": userid, "host": None})
    instance = await Instance.prisma().find_first(
        where={
            "isHere": True
        }
    )
    if user is None:
        return Response(status_code=404)
    if user.isInstanceActor:
        actor = {
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/v1",
            ],
            "id": f"https://{instance.host}/users/{user.id}",
            "type": "Application",
            "name": user.name,
            "preferredUsername": user.username,
            "inbox": f"https://{instance.host}/inbox",
            "outbox": f"https://{instance.host}/outbox",
            "icon": {
                "mediaType": user.avatarMediaType,
                "type": "Image",
                "url": user.avatarUrl
            },
            "publicKey": {
                "id": f"https://{instance.host}/users/{user.id}#main-key",
                "owner": f"https://{instance.host}/users/{user.id}",
                "publicKeyPem": user.publicKeyPem,
                "type": "Key"
            },
            "summary": user.description,
            "url": f"https://{instance.host}/about-Hol0?instance_actor=true",
        }
    else:
        actor = {
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/v1",
            ],
            "id": f"https://{instance.host}/users/{user.id}",
            "type": "Person",
            "name": user.name,
            "preferredUsername": user.username,
            "inbox": f"https://{instance.host}/{user.id}/inbox",
            "outbox": f"https://{instance.host}/{user.id}/outbox",
            "icon": {
                "mediaType": user.avatarMediaType,
                "type": "Image",
                "url": user.avatarUrl
            },
            "publicKey": {
                "id": f"https://{instance.host}/users/{user.id}#main-key",
                "owner": f"https://{instance.host}/users/{user.id}",
                "publicKeyPem": user.publicKeyPem,
                "type": "Key"
            },
            "summary": user.description,
            "url": f"https://{instance.host}/@{user.username}",
        }
    return ORJSONResponse(actor, media_type="application/activity+json")
"""
