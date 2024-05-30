import os

import orjson

import main

with open(os.path.join("./", "openapi.json"), "wb") as f:
    f.write(orjson.dumps(main.generate_schema()))
