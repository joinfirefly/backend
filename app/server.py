from contextlib import asynccontextmanager
import os
import urllib.parse
import logging

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from scalar_fastapi import get_scalar_api_reference
import prisma
import pyfiglet
from omegaconf import OmegaConf

from . import __version__, __codename__
from .utils import log

from . import routes

config = OmegaConf.load('./.config/config.yml')
logger, formatter = log.getLogger("HoloBE-Core")
handler = logging.FileHandler('./.logs/{:%Y-%m-%d}.log'.format(log.logConfig.time))
handler.setFormatter(formatter)
logger.addHandler(handler)

def generate_schema():
    Hol0_figlet = pyfiglet.figlet_format("Holo", font="chunky")
    logger.info("\n" + Hol0_figlet)
    logger.info(f"v{__version__}, Created By Holo Team")
    logger.info("Generating OpenAPI JSON...")
    openapi = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )
    logger.info("OpenAPI JSON data was successfully generated.")
    return openapi

@asynccontextmanager
async def lifespan(app: FastAPI):
    env = os.environ
    env["DATABASE_URL"] = f"postgresql://{urllib.parse.quote(config.database.user)}:{urllib.parse.quote(config.database.password)}@{config.database.host}:{config.database.port}/{urllib.parse.quote(config.database.name)}"
    db = prisma.Prisma(auto_register=True)
    await db.connect()
    await init()
    logger.info("server is running on: " + config.url)
    yield
    await db.disconnect()

app = FastAPI(
    title="Holo",
    description="An Interconnected Extensible Microblogging Platform🪐",
    version=__version__,
    lifespan=lifespan, 
    docs_url=None,
    redoc_url=None
)
app.include_router(routes.router)

@app.get("/api-doc", include_in_schema=False)
async def openapi_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
    
async def init():
    Hol0_figlet = pyfiglet.figlet_format("Holo", font="chunky")
    logger.info("\n" + Hol0_figlet)
    logger.info(f"v{__version__} ({__codename__}), Created By Holo Team")