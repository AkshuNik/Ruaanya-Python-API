from app.db.mongo import db
from datetime import datetime
from bson import ObjectId
import pytz, secrets, httpx
from app.models.apitoken_model import ApitokenInDB

IST = pytz.timezone("Asia/Kolkata")


class ApiTokenService:
    @staticmethod
    async def create_token(data, user_id):
        existing = await db["apitokens"].find_one({"user_id": user_id})
        if existing:
            return {"status": "IP Domain already exists"}

        token = None
        while not token:
            new_token = secrets.token_urlsafe(30)
            if not await db["apitokens"].find_one({"token": new_token}):
                token = new_token

        doc = {
            "token": token,
            "ip": str(data.ip),
            "domain": data.domain,
            "callbackurl": data.callbackurl,
            "redirecturl": data.redirecturl,
            "user_id": user_id,
            "created_at": datetime.now(IST),
            "updated_at": datetime.now(IST),
        }

        result = await db["apitokens"].insert_one(doc)
        return {"status": "success", "id": str(result.inserted_id)}

    @staticmethod
    async def list_tokens(user_id):
        tokens = []
        async for doc in db["apitokens"].find({"user_id": user_id}):
            doc["id"] = str(doc["_id"])
            doc["created_at"] = doc["created_at"].isoformat()
            doc["updated_at"] = doc["updated_at"].isoformat()
            tokens.append(doc)
        return tokens

    @staticmethod
    async def update_callback(user_id, callbackurl):
        test_payload = {
            "product": "test", "status": "test", "refno": "test", "txnid": "test"
        }
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(callbackurl, params=test_payload)
                if res.status_code != 200:
                    return {"status": "Callback user is not valid"}
        except:
            return {"status": "Callback validation failed"}

        await db["apitokens"].update_one({"user_id": user_id}, {"$set": {"callbackurl": callbackurl}})
        return {"status": "success"}

    @staticmethod
    async def update_company_code(user_id, companycode):
        await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": {"companycode": companycode}})
        return {"status": "success"}

    @staticmethod
    async def get_apitokens(user_id: str):
        tokens = await db["apitokens"].find({"user_id": user_id}).to_list(100)
        result = []
        for token in tokens:
            token["id"] = str(token["_id"])
            token["_id"] = str(token["_id"])
            token["user_id"] = str(token["user_id"])
            token["created_at"] = token["created_at"].isoformat()
            token["updated_at"] = token["updated_at"].isoformat()
            result.append(ApitokenInDB(**token))
        return result


    @staticmethod
    async def delete_token(token_id: str):
        try:
            obj_id = ObjectId(token_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid token ID format")

        result = await db["apitokens"].delete_one({"_id": obj_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="API token not found")

        return {"status": "success", "message": "API token deleted successfully"}