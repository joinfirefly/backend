from typing import Optional

from sqlmodel import Field, SQLModel
from python_aid import aidx

class BEConfig(SQLModel, table=True):
    id: Optional[str] = Field(default=aidx.genAidx(), primary_key=True)
    host: str = Field(unique=True)
    
    name: str = Field(default="Holo")
    description: str = Field(default="An Interconnected Extensible Microblogging Platform🪐")
    
    repositoryUrl: str = Field(default="https://github.com/hol0-dev/backend")
    feedbackUrl: str = Field(default="https://github.com/hol0-dev/backend/issues")
    
    admin: Optional[str] = Field(default=None)
    adminEmail: Optional[str] = Field(default=None)
    
    maintainer: Optional[str] = Field(default=None)
    maintainerEmail: Optional[str] = Field(default=None)
    
    impressumUrl: Optional[str] = Field(default=None)
    tosUrl: Optional[str] = Field(default=None)
    privacyPolicyUrl: Optional[str] = Field(default=None)
    
    pushNotification: bool = Field(default=False)
    swPublicKey: Optional[str] = Field(default=None)
    swPrivateKey: Optional[str] = Field(default=None)
    
    enableMail: bool = Field(default=False)
    mailAddress: Optional[str] = Field(default=None)
    smtpHost: Optional[str] = Field(default=None)
    smtpPort: Optional[str] = Field(default=None)
    smtpUser: Optional[str] = Field(default=None)
    smtpPass: Optional[str] = Field(default=None)
    smtpSSL: bool = Field(default=False)
    
    useObjectStrage: bool = Field(default=False)
    s3BaseUrl: Optional[str] = Field(default=None)
    s3Bucket: Optional[str] = Field(default=None)
    s3Prefix: Optional[str] = Field(default=None)
    s3Endpoint: Optional[str] = Field(default=None)
    s3Region: Optional[str] = Field(default="us-east-1")
    s3AccessKey: Optional[str] = Field(default=None)
    s3SecretKey: Optional[str] = Field(default=None)
    s3useSSL: bool = Field(default=False)
    s3ForcePathStyle: bool = Field(default=False)
    s3setPublicRead: bool = Field(default=False)
    
    enableTurnstile: bool = Field(default=False)
    turnstileSiteKey: Optional[str] = Field(default=None)
    turnstileSecretKey: Optional[str] = Field(default=None)

    faviconUrl: Optional[str] = Field(default=None)
    appleTouchIconUrl: Optional[str] = Field(default=None)
    androidTouchIconUrl: Optional[str] = Field(default=None)
    
    turnstileSecretKey: str = Field(default="#B0F7DD")