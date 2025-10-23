from pymongo import MongoClient, DESCENDING, ASCENDING
from .config import settings
from common.utils.mongo_helper import ensure_indexes

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
logs = db["audit_logs"]

ensure_indexes(logs, [
    ("timestamp", DESCENDING),
    ("modulo", ASCENDING),
    ("accion", ASCENDING),
    ("nivel_criticidad", ASCENDING)
])
