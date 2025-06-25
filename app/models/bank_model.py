from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BankBase(BaseModel):
    id: Optional[str]
    name: str
    account: str
    ifsc: str
    branch: str
    user_id: str
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class BankCreate(BaseModel):
    name: str
    account: str
    ifsc: str
    branch: str
    user_id: str
    status: str

class BankUpdate(BaseModel):
    id: str
    name: str
    account: str
    ifsc: str
    branch: str
    user_id: str
    status: str
