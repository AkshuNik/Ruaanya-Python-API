from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProviderBase(BaseModel):
    id: Optional[str]
    name: str
    plan: str
    operatorfind: str
    api_id: str
    type: str
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class ProviderCreate(BaseModel):
    name: str
    plan: str
    operatorfind: str
    api_id: str
    type: str
    status: str

class ProviderUpdate(BaseModel):
    id: str
    name: str
    plan: str
    operatorfind: str
    api_id: str
    type: str
    status: str
