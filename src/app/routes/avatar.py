from boringavatars import avatar
from robyn import SubRouter, Response
from prisma.models import User

from ..utils.responses import Redirect

router = SubRouter("Holo")


@router.get("/{username}.png")
async def get_avatar(username: str):
    user = await User.prisma().find_first(where={"username": username.lower()})
    if user is None:
        return Response(status_code=404)
    else:
        return Redirect(user.avatarUrl)

@router.get("/identicon/{text}/")
async def identicon(text: str):
    return Response(avatar(name=text), media_type="image/svg+xml")