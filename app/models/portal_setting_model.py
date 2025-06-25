from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PortalSettingBase(BaseModel):
    id: Optional[str]
    name: str
    code: str
    value: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class PortalSettingCreate(BaseModel):
    name: str
    code: str
    value: str

class PortalSettingUpdate(BaseModel):
    id: str
    name: str
    code: str
    value: str
