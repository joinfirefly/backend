from boringavatars import avatar
from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse
from prisma.models import User

router = APIRouter()

@router.get("/{username}.png")
async def get_avatar(username: str):
    user = await User.prisma().find_first(where={"username": username.lower()})
    if user is None:
        return Response(status_code=404)
    else:
        return RedirectResponse(user.avatarUrl)

@router.get("/identicon/{text}/")
async def identicon(text: str):
    return Response(avatar(name=text), media_type="image/svg+xml")