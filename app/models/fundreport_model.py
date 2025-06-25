from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FundReportBase(BaseModel):
    id: Optional[str]
    user_id: str
    ref_no: str
    amount: float
    payment_status: str
    remark: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class FundReportCreate(BaseModel):
    user_id: str
    ref_no: str
    amount: float
    payment_status: str
    remark: Optional[str]

class FundReportUpdate(BaseModel):
    id: str
    user_id: Optional[str]
    ref_no: Optional[str]
    amount: Optional[float]
    payment_status: Optional[str]
    remark: Optional[str]
