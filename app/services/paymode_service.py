from app.db.mongo import db
from datetime import datetime
from bson import ObjectId

class PaymodeService:

    @staticmethod
    async def create(data, user_id):
        payload = data.dict()
        payload["created_by"] = user_id
        payload["created_at"] = datetime.utcnow()
        result = await db.paymodes.insert_one(payload)
        return {"status": "success", "id": str(result.inserted_id)}

    @staticmethod
    async def list():
        paymodes = []
        cursor = db.paymodes.find()
        async for paymode in cursor:
            paymode["id"] = str(paymode["_id"])
            paymode.pop("_id", None)
            paymodes.append(paymode)
        return paymodes

    @staticmethod
    async def update(data, user_id):
        paymode_id = data.id
        update_data = {k: v for k, v in data.dict().items() if k != "id" and v is not None}
        update_data["updated_by"] = user_id
        update_data["updated_at"] = datetime.utcnow()

        result = await db.paymodes.update_one({"_id": ObjectId(paymode_id)}, {"$set": update_data})
        if result.modified_count == 1:
            return {"status": "success"}
        return {"status": "not modified"}

    @staticmethod
    async def delete(paymode_id):
        result = await db.paymodes.delete_one({"_id": ObjectId(paymode_id)})
        if result.deleted_count == 1:
            return {"status": "deleted"}
        return {"status": "not found"}
