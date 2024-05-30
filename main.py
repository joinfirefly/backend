import logging
import os
import sys
import urllib.parse
from contextlib import asynccontextmanager
from importlib import import_module

import pyfiglet
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

import config

coloredLog = {
    logging.DEBUG: "\033[94m",
    logging.INFO: "\033[32m",
    logging.WARNING: "\033[33m",
    logging.ERROR: "\033[31m",
    logging.CRITICAL: "\033[95m",
}

graphene_figlet = pyfiglet.figlet_format("Graphene", font="big")


class ColoredStreamHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            self.stream.write(coloredLog[record.levelno])
            super().emit(record)
        finally:
            self.stream.write("\033[0m")


def get(level=logging.INFO):
    logger = logging.getLogger("GrapheneBE")
    logger.setLevel(level)
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    if not logger.hasHandlers():
        handler = ColoredStreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)
    return logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("\n" + graphene_figlet)
    logger.info("v0.1.0, Created By AmaseCocoa")
    if config.debug:
        logger.warning(
            "Debug mode is enabled! To avoid data corruption, debug mode should only be used in a development environment!"
        )
    yield


app = FastAPI(lifespan=lifespan)
logLevel = logging.INFO
if config.debug:
    logLevel = logging.DEBUG
logger = get(logLevel)
if config.use_builtin_logger:

    @app.middleware("http")
    async def request_log(request: Request, call_next):
        params = dict(request.query_params)
        if params == {}:
            params = ""
        else:
            params = "?" + urllib.parse.urlencode(params)
        response: Response = await call_next(request)
        logger.info(
            f'"{request.method.upper()} {request.url.path}{params}" {response.status_code}'
        )
        return response

if config.frontend:
    app.mount(
        "/",
        StaticFiles(directory=os.path.join("./static", config.frontend), html=True),
        name="html",
    )
    logger.info(f"The Frontend “{config.frontend}” was successfully loaded.")

for file in os.listdir("./src"):
    if os.path.isfile(os.path.join("./src", file)):
        if file.endswith(".py"):
            module = import_module(f"src.{file[:-3]}")
            module.logger = logger
            if hasattr(module, 'graphene_on_load'):
                module.graphene_on_load()
            app.include_router(module.router)
    elif os.path.isdir(os.path.join("./src", file)):
        if file != "lib" or file != "__pycache__" or file != "models":
            for file_d in os.listdir(os.path.join("./src", file)):
                if os.path.isfile(os.path.join("./src", file_d)):
                    if file_d.endswith(".py"):
                        module = import_module(f"src.{file}.{file_d[:-3]}")
                        module.logger = logger
                        module.graphene_on_load()
                        app.include_router(module.router)

async def load_plugin():
    for file in os.listdir("./plugins"):
        if os.path.isfile(os.path.join("./plugins", file)):
            if file.endswith(".py"):
                module = import_module(f"plugins.{file[:-3]}")
                if hasattr(module, 'graphene_on_load'):
                    module.graphene_on_load()
                app.include_router(module.router)


def generate_schema():
    logger.info("\n" + graphene_figlet)
    logger.info("v0.1.0, Created By AmaseCocoa")
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


@app.get("/")
async def index():
    return {"Hello": "World"}
