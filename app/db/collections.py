from app.db.mongo import db

user_collection = db["users"]
role_collection = db["roles"]
transaction_collection = db["transactions"]
commissions_collection = db["commissions"]

