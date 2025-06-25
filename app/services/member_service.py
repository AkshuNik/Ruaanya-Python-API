import random
from app.models.user_model import MemberCreate, UserInDB
from app.db.mongo import db
from passlib.context import CryptContext
from datetime import datetime
from app.models.user_model import UserBase
import pytz
from bson import ObjectId

IST = pytz.timezone("Asia/Kolkata")
now_ist = datetime.now(IST)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class MemberService:
    @staticmethod
    async def create_member(data: MemberCreate, parent_user: dict):
        users_collection = db["users"]

        if await users_collection.find_one({"email": data.email}):
            return {"status": "Email already exists"}

        if await users_collection.find_one({"mobile": data.mobile}):
            return {"status": "Mobile already exists"}

        merchantcode = f"SUVI{random.randint(1111, 9999)}"
        hashed_password = pwd_context.hash(data.mobile)  # password = mobile

        new_user = {
            "name": data.name,
            "email": data.email,
            "mobile": data.mobile,
            "address": data.address,
            "state": data.state,
            "city": data.city,
            "pincode": data.pincode,
            "pancard": data.pancard,
            "aadharcard": data.aadharcard,
            "scheme_id": data.scheme_id,
            "role_id": data.role,  
            "parent_id": parent_user["_id"],
            "kyc": "verified",
            "password": hashed_password,
            "merchantcode": merchantcode,
            "created_at": now_ist,
            "updated_at": now_ist,
        }

        result = await users_collection.insert_one(new_user)

        if result.inserted_id:
            return {"status": "success", "user_id": str(result.inserted_id)}

        return {"status": "fail"}

    @staticmethod
    async def get_all_members():
        users_collection = db["users"]
        cursor = users_collection.find({"role_id": 2})
        members = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            members.append(UserBase(**doc))
        return members

    @staticmethod
    async def get_user_settings(id: str, current_user: dict):
        users_collection = db["users"]
        roles_collection = db["roles"]

        if id != "0":
            user = await users_collection.find_one({"_id": ObjectId(id)})
        else:
            user = current_user

        if not user:
            return {"status": "User not found"}

        data = {"user": user}

        if current_user.get("role_id") == 0:  # superadmin
            parents_cursor = users_collection.find({
                "role_id": {"$ne": 3}  # Assuming 3 is 'retailer'
            }, {"_id": 1, "name": 1, "role_id": 1, "mobile": 1})

            parents = await parents_cursor.to_list(length=None)

            roles_cursor = roles_collection.find({
                "slug": {"$ne": "admin"}
            })

            roles = await roles_cursor.to_list(length=None)

            data["parents"] = parents
            data["roles"] = roles
        else:
            data["parents"] = []
            data["roles"] = []

        return data
    
    @staticmethod
    async def profile_update(data, current_user):
        users_collection = db["users"]
        user_id = data.id

        # ✅ Role and permission checks (simplified)
        is_self = current_user["_id"] == user_id
        is_superadmin = current_user.get("role_id") == 0  # assume 0 is superadmin

        if not is_self and not is_superadmin:
            return {"status": "Permission Not Allowed"}

        update_data = {}
        now = datetime.utcnow()

        if data.actiontype == "password":
            if not is_superadmin:
                user = await users_collection.find_one({"_id": ObjectId(user_id)})
                if not user or not pwd_context.verify(data.oldpassword, user.get("password", "")):
                    return {"status": "Incorrect old password"}

            update_data["password"] = pwd_context.hash(data.password)
            update_data["passwordold"] = data.password
            update_data["resetpwd"] = "changed"

        elif data.actiontype == "profile":
            update_data.update({
                "name": data.name,
                "email": data.email,
                "mobile": data.mobile,
                "pancard": data.pancard,
                "aadharcard": data.aadharcard,
                "kyc": "verified"
            })

        elif data.actiontype == "bankdata":
            if not is_superadmin:
                return {"status": "Permission Not Allowed"}
            update_data.update({
                "bank_holder_name": data.bank_holder_name,
                "account": data.account,
                "bank": data.bank,
                "ifsc": data.ifsc
            })

        elif data.actiontype == "scheme":
            if not is_superadmin:
                return {"status": "Permission Not Allowed"}
            update_data["scheme_id"] = data.scheme_id
        
        elif data.actiontype == "status":
            if not is_superadmin:
                return {"status": "Permission Not Allowed"}
            update_data["status"] = data.status

        else:
            return {"status": "Invalid actiontype"}

        update_data["updated_at"] = now
        result = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        if result.modified_count:
            return {"status": "success"}
        return {"status": "fail"}