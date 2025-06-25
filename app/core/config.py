import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "My FastAPI App"
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "defaultsecret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

settings = Settings()
