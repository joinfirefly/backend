from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from ..utils.model_func import utcnow

if TYPE_CHECKING:
    from .instance import Instance
    from .note import Note
    from .user import User

class ChannelFollow(SQLModel, table=True):
    followee_id: str = Field(primary_key=True, index=True)
    channel_id: str = Field(foreign_key="channel.id", index=True)
    created_at: datetime = Field(default_factory=utcnow)

    channel: "Channel" = Relationship(sa_relationship_kwargs={"cascade": "all, delete"})
    followee: "User" = Relationship(back_populates="channel_followees", sa_relationship_kwargs={"cascade": "all, delete"})


class Channel(SQLModel, table=True):
    id: str = Field(primary_key=True, index=True)
    
    name: str
    description: str
    remote: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=utcnow, sa_column_kwargs={"name": "created_at"})
    updated_at: datetime = Field(default_factory=utcnow, sa_column_kwargs={"name": "updated_at", "onupdate": utcnow})

    host_id: Optional[str] = Field(default=None, foreign_key="instance.host")

    followers: List[ChannelFollow] = Relationship(back_populates="channel")
    notes: List["Note"] = Relationship(back_populates="channel")

# 補足としてUserとInstance、Noteのクラスも定義する必要がありますが、ここでは省略します。
