import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel
from python_aid import aidx

from ..utils.model_func import utcnow

if TYPE_CHECKING:
    from .channel import ChannelFollow
    from .instance import Instance
    from .note import Note, Reaction

class User(SQLModel, table=True):
    id: str = Field(default_factory=aidx.genAidx, primary_key=True)
    host: str
    username: str
    email: Optional[str] = Field(unique=True)
    password: Optional[str]
    displayName: Optional[str]
    description: Optional[str]
    avatarUrl: Optional[str]
    bannerUrl: Optional[str]
    bday: Optional[datetime.datetime]
    address: Optional[str]
    manuallyApprovesFollowers: bool = Field(default=False)
    discoverable: bool = Field(default=True)
    publicKeyPem: str
    publicKeyOwner: str
    privateKeyPem: Optional[str]
    accessTokens: List["AccessToken"] = Relationship(back_populates="user")
    channelFollowees: List["ChannelFollow"] = Relationship(back_populates="channelFollowee")
    notes: List["Note"] = Relationship(back_populates="user")
    reactions: List["Reaction"] = Relationship(back_populates="user")
    fields: List["Field"] = Relationship(back_populates="user")
    followees: List["Follow"] = Relationship(back_populates="follower")
    followers: List["Follow"] = Relationship(back_populates="followee")
    instance: Optional["Instance"] = Relationship(back_populates="users", field="host", remote_model="Instance")

class Field(SQLModel, table=True):
    id: str = Field(primary_key=True)
    authorId: str
    name: str
    value: str
    user: User = Relationship(back_populates="fields")

class Follow(SQLModel, table=True):
    followerId: str = Field(primary_key=True)
    followeeId: str = Field(primary_key=True)
    createdAt: datetime = Field(default_factory=utcnow)
    followee: User = Relationship(back_populates="followees", fields=[followeeId], references=[User.id], ondelete="CASCADE")
    follower: User = Relationship(back_populates="followers", fields=[followerId], references=[User.id], ondelete="CASCADE")

class AccessToken(SQLModel, table=True):
    id: str = Field(primary_key=True)
    createdAt: datetime = Field(default_factory=utcnow, alias="created_at")
    updatedAt: Optional[datetime.datetime] = Field(default=None, sa_column_kwargs={"onupdate": datetime.datetime.now(datetime.UTC)})
    expiresAt: Optional[datetime.datetime]
    name: str
    scope: List[str]
    token: str = Field(unique=True)
    userId: str = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="accessTokens", fields=[userId], references=[User.id], ondelete="CASCADE")
    fromWeb: bool = Field(default=False)
