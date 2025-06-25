from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApiBase(BaseModel):
    id: Optional[str]
    product: str
    name: str
    url: str
    username: str
    password: str
    optional1: Optional[str] = None
    optional2: Optional[str] = None
    code: str
    type: str
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class ApiCreate(BaseModel):
    product: str
    name: str
    url: str
    username: str
    password: str
    optional1: Optional[str] = None
    optional2: Optional[str] = None
    code: str
    type: str
    status: str

class ApiUpdate(BaseModel):
    id: str
    product: str
    name: str
    url: str
    username: str
    password: str
    optional1: Optional[str] = None
    optional2: Optional[str] = None
    code: str
    type: str
    status: str
