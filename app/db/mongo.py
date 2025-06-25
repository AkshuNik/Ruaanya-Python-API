# from pymongo import MongoClient
# from app.core.config import settings

# # MongoDB client instance
# client = MongoClient(settings.MONGO_URI)

# # Specific database (example: myproject)
# db = client["suvidhaabnk"]

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["suvidhaabnk"]
