import os
import shutil

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
        
combine_schema()