from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PermissionBase(BaseModel):
    id: Optional[str]
    name: str
    slug: str
    type: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class PermissionCreate(BaseModel):
    name: str
    slug: str
    type: str

class PermissionUpdate(BaseModel):
    id: str
    name: str
    slug: str
    type: str
