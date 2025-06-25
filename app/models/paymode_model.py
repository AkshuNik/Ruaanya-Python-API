from pydantic import BaseModel
from typing import Optional

class PaymodeCreate(BaseModel):
    name: str
    status: bool

class PaymodeUpdate(BaseModel):
    id: str
    name: Optional[str]
    status: Optional[bool]
