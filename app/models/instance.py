from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User

class Instance(SQLModel, table=True):
    id: str = Field(primary_key=True)
    host: str = Field(unique=True)
    usersCount: int = Field(default=0)
    notesCount: int = Field(default=0)
    name: Optional[str]
    description: Optional[str]
    iconUrl: str
    faviconUrl: str
    themeColor: str = Field(default="#ffffff")
    firstRetrievedAt: Optional[datetime] = Field(default=datetime.now())
    isNotResponding: Optional[bool] = Field(default=False)
    isSuspended: Optional[bool] = Field(default=False)
    isBlocked: Optional[bool] = Field(default=False)
    isSilenced: Optional[bool] = Field(default=False)
    softwareName: Optional[str]
    softwareVersion: Optional[str]
    softwareHomepage: Optional[str]
    openRegistrations: bool
    adminName: Optional[str]
    adminEmail: Optional[str]
    maintainerName: Optional[str]
    maintainerEmail: Optional[str]
    infoUpdatedAt: datetime = Field(default=datetime.now())
    latestRequestReceivedAt: datetime = Field(default=datetime.now())
    moderationNote: Optional[str]
    langs: List[str]
    tosUrl: Optional[str]
    privacyPolicyUrl: Optional[str]
    inquiryUrl: Optional[str]
    impressumUrl: Optional[str]
    repositoryUrl: Optional[str]
    feedbackUrl: Optional[str]

    users: List["User"] = Relationship(back_populates="instance", field="host", remote_model="User")
