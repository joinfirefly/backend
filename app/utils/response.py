from typing import Optional, Union

from fastapi import Response
from starlette.background import BackgroundTask

class XMLResponse(Response):
    def __init__(
        self,
        content: Union[str, bytes],
        status_code: int = 200,
        background: Optional[BackgroundTask] = None,
    ):
        super().__init__(
            content,
            status_code=status_code,
            media_type="application/xml",
            background=background,
        )