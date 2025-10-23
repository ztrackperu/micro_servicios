from datetime import datetime
from bson import ObjectId

def normalize_user(doc: dict) -> dict:
    if not doc: return None
    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    return doc

def new_user_doc(data: dict) -> dict:
    return {
        "email": data["email"].lower(),
        "password_hash": data["password_hash"],
        "nombre": data["nombre"],
        "apellido": data["apellido"],
        "rol": data.get("rol","CLIENT"),
        "empresa_id": data.get("empresa_id"),
        "activo": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

def update_user_doc(data: dict) -> dict:
    upd = {k:v for k,v in data.items() if v is not None and k!="id"}
    if upd: upd["updated_at"] = datetime.utcnow()
    return {"$set": upd}
