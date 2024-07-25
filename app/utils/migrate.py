import asyncio
import os
import urllib.parse
import subprocess
import shutil
import importlib

from yarl import URL
from omegaconf import OmegaConf
from prisma_cleanup import cleanup

config = OmegaConf.load('./.config/config.yml')

def combine_schema():
    schemas = "\n\n"
    try:
        shutil.rmtree("./prisma", ignore_errors=True)
    except FileNotFoundError:
        pass
    os.makedirs("./prisma", exist_ok=True)
    for f in os.listdir("./app/models/prisma"):
        if os.path.isfile(os.path.join("./app/models/prisma", f)) and f.endswith(".prisma"):
            with open(os.path.join("./app/models/prisma", f), "r", encoding="utf-8") as schema:
                schemas += schema.read() + "\n\n"
    with open("./app/models/prisma/schema.tmpl", "r", encoding="utf-8") as p:
        prisma_tmpl = p.read()
    with open("./prisma/schema.prisma", "w", encoding="utf-8") as f:
        f.write(prisma_tmpl + schemas)

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

cleanup()
combine_schema()
env = os.environ
env["DATABASE_URL"] = f"postgresql://{urllib.parse.quote(config.database.user)}:{urllib.parse.quote(config.database.password)}@{config.database.host}:{config.database.port}/{urllib.parse.quote(config.database.name)}"
subprocess.run("prisma db push", env=env)
asyncio.run(setup())