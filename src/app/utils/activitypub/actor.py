import asyncio

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from prisma.models import User
from python_aid import aidx
from yarl import URL

from ... import __version__
from ..exceptions import HostNotFoundError, WebFingerNotSupported, ActorNotFound, RemoteActorException


async def get_remote_user(host: str, handle: str):
    actor = await User.prisma().find_first(
        where={
            "host": host,
            "handle": handle
        }
    )
    if actor is None:
        actor = await fetch_remote_actor(host, handle)

async def get_remote_user_from_url(url: str):
    actor = await User.prisma().find_first(
        where={
            "actorUrl": url
        }
    )
    remote = URL(url)
    if actor is None:
        async with aiohttp.ClientSession() as session:
            raw_actor = fetch_remote_actor_from_url(url, session)
            if raw_actor.get("icon"):
                if raw_actor["icon"].get("url"):
                    avatarUrl = raw_actor["icon"].get("url")
                else:
                    avatarUrl = None
            else:
                avatarUrl = None
            if raw_actor.get("image"):
                if raw_actor["image"].get("url"):
                    bannerUrl = raw_actor["image"].get("url")
                else:
                    bannerUrl = None
            else:
                bannerUrl = None
            if raw_actor.get("summary"):
                description = raw_actor.get("summary")
            else:
                description = ""
            actor = await User.prisma().create(
                data={
                    "id": aidx.genAidx(),
                    "host": remote.host,
                    "username": raw_actor["preferredUsername"],
                    "normalizedUserName": raw_actor["preferredUsername"].lower(),
                    "avatarUrl": avatarUrl,
                    "bannerUrl": bannerUrl,
                    "description": description,
                    "manuallyApprovesFollowers": raw_actor.get("manuallyApprovesFollowers", False),
                    "discoverable": raw_actor.get("discoverable", False),
                    "publicKeyOwner": raw_actor["publicKey"]["owner"],
                    "publicKeyPem": raw_actor["publicKey"]["publicKeyPem"],
                    "bday": raw_actor.get("vcard:bday"),
                    "address": raw_actor.get("vcard:Address")
                }
            )
    return actor

async def fetch_remote_actor_from_url(url: str, session: aiohttp.ClientSession):
    async with session.get(url, headers={"User-Agent": f"Hol0/{__version__} ()", "Accept": "application/activity+json"}) as resp:
        if resp.status != 200:
            raise RemoteActorException
        actor = await resp.json()
        if "https://www.w3.org/ns/activitystreams" in actor["@context"]:
            return actor
        else:
            raise ActorNotFound

async def fetch_remote_actor(host: str, handle: str, acct_host: str=None):
    if acct_host is None:
        acct_host = host
    try:
        async with aiohttp.ClientSession(headers={"User-Agent": f"Hol0/{__version__} ()"}) as session:
            async with session.get(f"https://{host}/.well-known/webfinger?resource=acct:{handle}@{acct_host}") as resp:
                if resp.status == 404:
                    raise ActorNotFound
                elif resp.status != 200:
                    raise WebFingerNotSupported
                wf = await resp.json()
                if wf["subject"] == f"acct:{handle}@{acct_host}":
                    for link in wf["links"]:
                        if link["type"] == "application/activity+json":
                            actor_url = link["href"]
                            actor = await fetch_remote_actor_from_url(actor_url, session)
                            break
                    return actor
    except ClientConnectorError:
        raise HostNotFoundError(f"Host: {host} is unavailable")
    
asyncio.run(get_remote_user_from_url("https://misskey.io/users/9sx9majyf5k302i8"))