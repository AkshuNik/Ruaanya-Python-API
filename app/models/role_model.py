from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RoleBase(BaseModel):
    name: str
    slug: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    id: str

class RoleOut(RoleBase):
    id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
