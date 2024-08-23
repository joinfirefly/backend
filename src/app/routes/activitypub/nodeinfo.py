import logging

from robyn import SubRouter, Request, jsonify

from prisma.models import BEConfig, User, Note

from ... import __version__

router = SubRouter("Holo", prefix="/nodeinfo")

logger: logging.Logger = None


@router.get("/2.1")
async def v2_1(request: Request):
    users = await User.prisma().count()
    notes = await Note.prisma().count()
    instance = await BEConfig.prisma().find_first(where={"id": "hol0"})
    ni = {
        "version": "2.1",
        "software": {
            "name": "Holo",
            "version": __version__,
            "repository": instance.repositoryUrl,
            "homepage": "https://join.hol0.dev",
        },
        "protocols": ["activitypub"],
        "services": {"inbound": [], "outbound": []},
        "openRegistrations": False,
        "usage": {
            "users": {"total": users, "activeHalfyear": None, "activeMonth": None},
            "localPosts": notes,
            "localComments": 0,
        },
        "metadata": {
            "nodeName": instance.name,
            "nodeDescription": instance.description,
            "nodeAdmins": [],
            "langs": ["ja"],
            "tosUrl": instance.tosUrl,
            "privacyPolicyUrl": instance.privacyPolicyUrl,
            "impressumUrl": instance.impressumUrl,
            "repositoryUrl": instance.repositoryUrl,
            "feedbackUrl": instance.feedbackUrl,
            "themeColor": "#b0e0e6",
            "enableTurnstile": instance.enableTurnstile
        },
    }
    if instance.admin:
        if instance.adminEmail:
            ni["metadata"]["nodeAdmins"].append(
                {
                    "name": instance.admin, 
                    "email": instance.adminEmail
                }
            )
        else:
            ni["metadata"]["nodeAdmins"].append(
                {
                    "name": instance.admin
                }
            )
    if instance.maintainerName:
        if instance.maintainerEmail:
            ni["maintainer"] = {
                "name": instance.maintainerName, 
                "email": instance.maintainerEmail
            }
        else:
            ni["maintainer"] = {
                "name": instance.maintainerName
            }
    return ni


@router.get("/2.0")
async def v2(request: Request):
    users = await User.prisma().count()
    notes = await Note.prisma().count()
    instance = await BEConfig.prisma().find_first(where={"id": "hol0"})
    ni = {
            "version": "2.0",
            "software": {
                "name": "Holo",
                "version": __version__,
            },
            "protocols": ["activitypub"],
            "services": {"inbound": [], "outbound": []},
            "openRegistrations": False,
            "usage": {
                "users": {"total": users, "activeHalfyear": None, "activeMonth": None},
                "localPosts": notes,
                "localComments": 0,
            },
            "metadata": {
                "nodeName": instance.name,
                "nodeDescription": instance.description,
                "nodeAdmins": [],
                "langs": ["ja"],
                "repositoryUrl": instance.repositoryUrl,
                "tosUrl": instance.tosUrl,
                "feedbackUrl": instance.feedbackUrl,
                "themeColor": instance.themeColor,
            },
        }
    if instance.admin:
        if instance.adminEmail:
            ni["metadata"]["nodeAdmins"].append(
                {
                    "name": instance.admin, 
                    "email": instance.adminEmail
                }
            )
        else:
            ni["metadata"]["nodeAdmins"].append(
                {
                    "name": instance.admin
                }
            )
    if instance.maintainerName:
        if instance.maintainerEmail:
            ni["maintainer"] = {
                "name": instance.maintainerName, 
                "email": instance.maintainerEmail
            }
        else:
            ni["maintainer"] = {
                "name": instance.maintainerName
            }
    return ni