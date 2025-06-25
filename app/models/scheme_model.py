from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SchemeBase(BaseModel):
    id: Optional[str]
    name: str
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class SchemeCreate(BaseModel):
    name: str
    status: str

class SchemeUpdate(BaseModel):
    id: str
    name: str
    status: str
