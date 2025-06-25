from fastapi import HTTPException, Request
from app.db.mongo import db
from app.models.user_model import UserCreate, UserLogin, UserInDB
from app.utils.jwt import create_access_token
from passlib.context import CryptContext
from fastapi import HTTPException
from datetime import datetime



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    async def register_user(user: UserCreate):
        existing_user = await db["users"].find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # ✅ Check if mobile already exists
        existing_mobile = await db["users"].find_one({"mobile": user.mobile})
        if existing_mobile:
            raise HTTPException(status_code=400, detail="Mobile number already registered")
        
        user_dict = user.dict()
        user_dict["password"] = pwd_context.hash(user.password)
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()
        user_dict["kyc"] = "pending"
        # user_dict["role_id"] = 1

        new_user = await db["users"].insert_one(user_dict)
        created_user = await db["users"].find_one({"_id": new_user.inserted_id})
        return UserInDB(**created_user)

    @staticmethod
    async def login_user(user: UserLogin):
        # existing_user = await db["users"].find_one({"email": user.email})
        existing_user = await db["users"].find_one({
            "$or": [
                {"email": user.email_or_mobile},
                {"mobile": user.email_or_mobile}
            ]
        })
        if not existing_user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        user_in_db = UserInDB(**existing_user)

        if not pwd_context.verify(user.password, user_in_db.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = create_access_token(data={"sub": str(user_in_db.id)})
        return {
            "access_token": token, 
            "token_type": "bearer",
                "user": {
                    "id": str(user_in_db.id),
                    "name": user_in_db.name,
                }
            }

    @staticmethod
    async def logout_user(request: Request):
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing token")

        token = auth_header.split(" ")[1]
        
        # Token blacklist kar do
        await db["token_blacklist"].insert_one({"token": token})
        return {"detail": "Logout successful"}
