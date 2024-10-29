from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client.cloud_security  # MongoDB Atlas database instance