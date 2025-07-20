from pydantic import BaseModel, Field
from typing import Optional, Dict

class RegistrarLoginSchema(BaseModel):
    username: str
    password: str

class CertificateRequestSchema(BaseModel):
    userId: str
    applicationNumber: str
    certificateType: str  # BIRTH, DEATH, MARRIAGE, RESIDENCE
    status: str
    assignedRegistrarId: Optional[str]
    data: Dict  # flexible data

class CertificateStatusUpdate(BaseModel):
    status: str
