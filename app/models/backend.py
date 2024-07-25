from typing import Optional

from sqlmodel import Field, SQLModel
from python_aid import aidx

class BEConfig(SQLModel, table=True):
    id: Optional[str] = Field(default=aidx.genAidx(), primary_key=True)
    host: str = Field(unique=True)
    name: str = Field(default="Holo")
    description: str = Field(default="An Interconnected Extensible Microblogging Platform🪐")