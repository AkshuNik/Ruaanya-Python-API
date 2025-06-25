# app/models/company_model.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CompanyBase(BaseModel):
    id: Optional[str]
    companyname: str
    shortname: str
    website: str
    logo: Optional[str]
    status: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class CompanyCreate(BaseModel):
    companyname: str
    shortname: str
    website: str
    logo: Optional[str]
    status: bool

class CompanyUpdate(CompanyCreate):
    id: str
