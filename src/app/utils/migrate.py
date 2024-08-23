import asyncio
import os
import urllib.parse
import subprocess
import importlib

from yarl import URL
from omegaconf import OmegaConf
# from prisma_cleanup import cleanup

config = OmegaConf.load('./.config/config.yml')

async def setup():
    prisma = importlib.import_module('prisma')
    db = prisma.Prisma()
    await db.connect()
    instance = await db.beconfig.find_first(
        where={
            "id": "hol0"
        }
    )
    if instance is None:
        url = URL(config.url)
        instance = await db.beconfig.create(
            data={
                "id": "hol0",
                "host": url.host,
                "name": url.host
            }
        )

# cleanup()
env = os.environ
env["DATABASE_URL"] = f"postgresql://{urllib.parse.quote(config.database.user)}:{urllib.parse.quote(config.database.password)}@{config.database.host}:{config.database.port}/{urllib.parse.quote(config.database.name)}"
subprocess.run("prisma db push", env=env)
asyncio.run(setup())