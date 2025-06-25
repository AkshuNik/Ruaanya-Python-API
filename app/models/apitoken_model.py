from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class ApitokenCreate(BaseModel):
    ip: str
    domain: str
    callbackurl: Optional[str] = None
    redirecturl: Optional[str] = None


class CallbackUpdate(BaseModel):
    callbackurl: str


class CompanyCodeUpdate(BaseModel):
    companycode: str


class ApitokenInDB(BaseModel):
    id: str = Field(..., alias="_id")
    token: str
    ip: str
    domain: str
    callbackurl: Optional[str]
    redirecturl: Optional[str]
    user_id: str
    created_at: str
    updated_at: str

    class Config:
        # allow_population_by_field_name = True
        validate_by_name  = True
        json_encoders = {
            ObjectId: str
        }
