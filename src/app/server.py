from contextlib import asynccontextmanager
import os
import urllib.parse
import logging

from robyn import Robyn, Request, Response #, OpenAPI
# from robyn.openapi import OpenAPIInfo, Contact, License, ExternalDocumentation, Components

import prisma
import pyfiglet
from omegaconf import OmegaConf

from . import __version__, __codename__
from .utils import log

from . import routes

config = OmegaConf.load('./.config/config.yml')
logger, formatter = log.getLogger("Holo")
db = prisma.Prisma(auto_register=True)
handler = logging.FileHandler('./.logs/{:%Y-%m-%d}.log'.format(log.logConfig.time))
handler.setFormatter(formatter)
logger.addHandler(handler)

def generate_schema():
    Hol0_figlet = pyfiglet.figlet_format("Holo", font="chunky")
    logger.info("\n" + Hol0_figlet)
    logger.info(f"v{__version__}, Created By Holo Team")
    logger.info("Generating OpenAPI JSON...")
    """
    openapi = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )
    """
    logger.info("OpenAPI JSON data was successfully generated.")
#     return openapi


"""
app = FastAPI(
    title="Holo",
    description="An Interconnected Extensible Microblogging Platform🪐",
    version=__version__,
    lifespan=lifespan, 
    docs_url=None,
    redoc_url=None
)

app.include_router(routes.router)
"""
app = Robyn(
    file_object="Holo",
#    openapi=OpenAPI(
#        info=OpenAPIInfo(
#            title="Holo",
#            description="An Interconnected Extensible Microblogging Platform🪐",
#            version=__version__,
#            contact=Contact(
#                name="holo-social",
#                url="https://github.com/holo-social/backend/issues/new",
#            ),
#            license=License(
#                name="AGPL-3.0",
#                url="https://opensource.org/license/agpl-v3",
#            ),
#            externalDocs=ExternalDocumentation(description="Find more info here", url="https://docs.hol0.dev/"),
#            components=Components(),
#        ),
#    ),
)
app.include_router(routes.router)

@app.before_request()
async def log_request(request: Request):
    logger.info(
        f' {request.ip_addr if request.ip_addr else "unknown"} - {request.method.upper()} {request.url.path}'
    )
    return request

@app.startup_handler
async def startup_handler() -> None:
    env = os.environ
    env["DATABASE_URL"] = f"postgresql://{urllib.parse.quote(config.database.user)}:{urllib.parse.quote(config.database.password)}@{config.database.host}:{config.database.port}/{urllib.parse.quote(config.database.name)}"
    await db.connect()
    await init()
    logger.info("server is running on: " + config.url)


@app.shutdown_handler
async def shutdown_handler() -> None:
    if db.is_connected():
        await db.disconnect()

"""
@app.get("/api-doc", include_in_schema=False)
async def openapi_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
"""

async def init():
    Hol0_figlet = pyfiglet.figlet_format("Holo", font="chunky")
    logger.info("\n" + Hol0_figlet)
    logger.info(f"v{__version__} ({__codename__}), Created By Holo Team")