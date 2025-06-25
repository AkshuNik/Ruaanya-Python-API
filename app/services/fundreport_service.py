from app.db.mongo import db
from bson import ObjectId
from datetime import datetime
from app.models.fundreport_model import FundReportCreate, FundReportUpdate, FundReportBase

class FundReportService:
    collection_name = "fundreports"

    @staticmethod
    async def create_fundreport(data: FundReportCreate):
        collection = db[FundReportService.collection_name]
        now = datetime.utcnow()
        new_data = data.dict()
        new_data.update({"created_at": now, "updated_at": now})

        result = await collection.insert_one(new_data)
        return {"status": "success", "id": str(result.inserted_id)}

    @staticmethod
    async def get_all_fundreports():
        collection = db[FundReportService.collection_name]
        cursor = collection.find()
        reports = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            reports.append(FundReportBase(**doc))
        return reports

    @staticmethod
    async def update_fundreport(data: FundReportUpdate):
        collection = db[FundReportService.collection_name]
        update_data = data.dict(exclude={"id"}, exclude_unset=True)
        if not update_data:
            return {"status": "no fields to update"}
        update_data["updated_at"] = datetime.utcnow()

        result = await collection.update_one({"_id": ObjectId(data.id)}, {"$set": update_data})
        if result.modified_count:
            return {"status": "success"}
        return {"status": "not updated"}

    @staticmethod
    async def delete_fundreport(id: str):
        collection = db[FundReportService.collection_name]
        result = await collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return {"status": "success"}
        return {"status": "not deleted"}
