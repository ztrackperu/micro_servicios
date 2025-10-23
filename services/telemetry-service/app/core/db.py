from pymongo import MongoClient, ASCENDING, DESCENDING
from .config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

def month_coll(prefix: str, dt) -> str:
    return f"{prefix}_{dt.year}_{dt.month:02d}"
