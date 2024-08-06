from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel
from python_aid import aidx

from ..utils.model_func import utcnow

if TYPE_CHECKING:
    from .channel import Channel
    from .instance import Instance
    from .user import User

class Reactions(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    noteId: str = Field(foreign_key="note.id")
    userId: str = Field(foreign_key="user.id")

    note: "Note" = Relationship(back_populates="reactions")
    user: "User" = Relationship(back_populates="reactions", sa_relationship_kwargs={"cascade": "all, delete"})

class File(SQLModel, table=True):
    id: str = Field(default_factory=aidx.genAidx, primary_key=True)
    hash: str = Field(unique=True)
    url: str
    isSensitive: bool
    fileSize: Optional[int] = None
    fileType: str
    caption: Optional[str] = None
    createdAt: datetime = Field(default_factory=utcnow)
    attachedNotes: List["Note"] = Relationship(back_populates="attachments", link_model="AttachmentsToNote")

class Note(SQLModel, table=True):
    id: str = Field(default_factory=aidx.genAidx, primary_key=True)
    content: Optional[str] = None
    content_html: Optional[str] = None
    username: str
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    visibility: str
    visibleUserIds: List[str] = []
    replyId: Optional[str] = None
    renoteId: Optional[str] = None
    channelId: Optional[str] = Field(default=None, foreign_key="channel.id")
    channel: Optional["Channel"] = Relationship(back_populates="notes")
    authorId: str = Field(foreign_key="user.id")
    author: "User" = Relationship(back_populates="notes")
    reactions: List["Reactions"] = Relationship(back_populates="note")
    attachments: List["File"] = Relationship(back_populates="note")