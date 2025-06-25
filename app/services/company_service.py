# app/services/company_service.py
from app.db.mongo import db
from bson import ObjectId
from datetime import datetime
from app.models.company_model import CompanyCreate, CompanyUpdate, CompanyBase

class CompanyService:
    @staticmethod
    async def create_company(data: CompanyCreate):
        collection = db["company_profile"]
        now = datetime.utcnow()
        company_data = data.dict()
        company_data.update({"created_at": now, "updated_at": now})
        result = await collection.insert_one(company_data)
        return {"status": "success", "id": str(result.inserted_id)}

    @staticmethod
    async def get_all_companies():
        collection = db["company_profile"]
        companies = []
        async for doc in collection.find():
            doc["id"] = str(doc["_id"])
            companies.append(CompanyBase(**doc))
        return companies

    @staticmethod
    async def update_company(data: CompanyUpdate):
        collection = db["company_profile"]
        update_data = data.dict()
        company_id = update_data.pop("id")
        update_data["updated_at"] = datetime.utcnow()
        result = await collection.update_one({"_id": ObjectId(company_id)}, {"$set": update_data})
        if result.modified_count:
            return {"status": "success"}
        return {"status": "not updated"}

    @staticmethod
    async def delete_company(id: str):
        collection = db["company_profile"]
        result = await collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return {"status": "success"}
        return {"status": "not deleted"}
