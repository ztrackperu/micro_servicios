from . import db
from bson import ObjectId
from app.models.user_model import normalize_user, new_user_doc, update_user_doc
from common.utils.security import hash_password, verify_password

def create_user(email: str, password: str, nombre: str, apellido: str, rol: str, empresa_id: str | None):
    if db.users_col.find_one({"email": email.lower()}):
        raise ValueError("Email ya existe")
    doc = new_user_doc({
        "email": email,
        "password_hash": hash_password(password),
        "nombre": nombre,
        "apellido": apellido,
        "rol": rol,
        "empresa_id": empresa_id
    })
    res = db.users_col.insert_one(doc)
    return normalize_user(db.users_col.find_one({"_id": res.inserted_id}))

def authenticate(email: str, password: str):
    user = db.users_col.find_one({"email": email.lower(), "activo": True})
    if not user: return None
    if not verify_password(password, user["password_hash"]):
        return None
    return normalize_user(user)

def get_user(uid: str):
    doc = db.users_col.find_one({"_id": ObjectId(uid)})
    return normalize_user(doc)

def list_users(skip=0, limit=50, q: str | None=None, rol: str | None=None, activo: bool | None=None):
    filt = {}
    if q: filt["$or"] = [{"email":{"$regex":q,"$options":"i"}},{"nombre":{"$regex":q,"$options":"i"}},{"apellido":{"$regex":q,"$options":"i"}}]
    if rol: filt["rol"] = rol
    if activo is not None: filt["activo"] = activo
    cur = db.users_col.find(filt).skip(skip).limit(limit).sort("created_at",-1)
    return [normalize_user(x) for x in cur]

def update_user(uid: str, data: dict):
    if "password" in data and data["password"]:
        data["password_hash"] = hash_password(data.pop("password"))
    res = db.users_col.update_one({"_id": ObjectId(uid)}, update_user_doc(data))
    if not res.matched_count:
        return None
    return get_user(uid)

def delete_user(uid: str):
    res = db.users_col.delete_one({"_id": ObjectId(uid)})
    return res.deleted_count == 1
