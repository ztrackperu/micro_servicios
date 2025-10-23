from pymongo import MongoClient
from .config import settings
from common.utils.mongo_helper import ensure_indexes
from datetime import datetime

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

users_col = db["usuarios"]
sessions_col = db["sesiones"]
roles_col = db["roles_permisos"]

# índices
ensure_indexes(users_col, [
    ("email", 1), ("rol", 1), ("activo", 1), ("empresa_id", 1), ("created_at", -1)
], unique=["email"])

ensure_indexes(sessions_col, [("user_id",1), ("activa",1), ("fecha_expiracion",1)])
ensure_indexes(roles_col, [("nombre",1)], unique=["nombre"])

# bootstrap rol ADMIN si no existe
if not roles_col.find_one({"nombre":"ADMIN"}):
    roles_col.insert_one({
        "nombre":"ADMIN",
        "permisos": {"usuarios":{"crear":True,"editar":True,"ver":True,"eliminar":True}},
        "activo": True,
        "created_at": datetime.utcnow()
    })
