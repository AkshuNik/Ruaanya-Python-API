from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from pydantic import GetJsonSchemaHandler
from pydantic_core import core_schema

# ✅ Pydantic v2 compatible ObjectId class
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetJsonSchemaHandler):
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.is_instance_schema(ObjectId),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

# ✅ Base model for shared fields
class UserBase(BaseModel):
    # merchantcode: Optional[str] = ""
    # name: Optional[str] = ""
    # email: Optional[EmailStr] = ""
    # mobile: Optional[str] = ""
    # role_id: Optional[int] = 1
    # password: Optional[str] = ""
    # kyc: Optional[str] = "pending"
    # status: Optional[str] = ""
    # mainwallet: Optional[float] = 0
    # payinwallet: Optional[float] = 0
    # suvidhawallet: Optional[float] = 0
    # lockedamount: Optional[float] = 0
    # created_at: Optional[datetime] = None
    # updated_at: Optional[datetime] = None
    _id: Optional[str] = None
    merchantcode: Optional[str] = ""
    name: Optional[str] = ""
    email: Optional[EmailStr] = ""
    mobile: Optional[str] = ""
    password: Optional[str] = ""
    remember_token: Optional[str] = None
    otpverify: Optional[str] = ""
    otpresend: Optional[int] = 0
    mainwallet: Optional[float] = 0
    payinwallet: Optional[float] = 0
    suvidhawallet: Optional[float] = 0
    lockedamount: Optional[float] = 0
    role_id: Optional[int] = 1
    parent_id: Optional[str] = "0"
    company_id: Optional[str] = None
    scheme_id: Optional[str] = None
    payin_api: Optional[str] = ""
    payout_api: Optional[str] = ""
    status: Optional[str] = ""
    address: Optional[str] = None
    shopname: Optional[str] = None
    gstin: Optional[str] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    pancard: Optional[str] = None
    aadharcard: Optional[str] = None
    pancardpic: Optional[str] = None
    aadharcardpic: Optional[str] = None
    gstpic: Optional[str] = None
    profile: Optional[str] = None
    profilepic: Optional[str] = None
    kyc: Optional[str] = "pending"
    callbackurl: Optional[str] = None
    remark: Optional[str] = None
    resetpwd: Optional[str] = "default"
    bank_holder_name: Optional[str] = None
    account: Optional[str] = None
    bank: Optional[str] = None
    ifsc: Optional[str] = None
    passwordold: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    access_token: Optional[str] = None
    expires_at: Optional[datetime] = None

# ✅ Model used internally with _id
class UserInDB(UserBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        validate_by_name = True              # ✅ replaces old `populate_by_name`
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# ✅ For registration input
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    mobile: str
    password: str

# ✅ For login input
class UserLogin(BaseModel):
    email_or_mobile: str
    password: str

class MemberCreate(BaseModel):
    name: str
    email: EmailStr
    mobile: str
    address: str
    state: str
    city: str
    pincode: str
    pancard: str
    aadharcard: str
    scheme_id: str
    role: str 

class ProfileUpdateRequest(BaseModel):
    id: str
    actiontype: str
    oldpassword: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    pancard: Optional[str] = None
    aadharcard: Optional[str] = None
    bank_holder_name: Optional[str] = None
    account: Optional[str] = None
    bank: Optional[str] = None
    ifsc: Optional[str] = None
    scheme_id: Optional[str] = None
    status: Optional[str] = None

