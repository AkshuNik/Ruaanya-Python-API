from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CommissionBase(BaseModel):
    id: Optional[str]
    type: str
    slab: str
    apiuser: str
    scheme_id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class CommissionCreate(BaseModel):
    type: str
    slab: str
    apiuser: str
    scheme_id: str

class CommissionUpdate(BaseModel):
    id: str
    type: str
    slab: str
    apiuser: str
    scheme_id: str

# class CommissionBase(BaseModel):
#     id: Optional[str]
#     type: str
#     slab: str
#     apiuser: str
#     mode: str         # ✅ ADD THIS
#     scheme_id: str
#     created_at: Optional[datetime]
#     updated_at: Optional[datetime]

# class CommissionCreate(BaseModel):
#     type: str
#     slab: str
#     apiuser: str
#     mode: str         # ✅ ADD THIS
#     scheme_id: str

# class CommissionUpdate(BaseModel):
#     id: str
#     type: str
#     slab: str
#     apiuser: str
#     mode: str         # ✅ ADD THIS
#     scheme_id: str