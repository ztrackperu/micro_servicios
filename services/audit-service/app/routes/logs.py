from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId
from app.core.db import logs
from common.schemas.audit_schema import AuditLogIn

router = APIRouter(prefix="/api/audit", tags=["Audit"])

@router.post("/logs")
def push_log(payload: AuditLogIn):
    doc = payload.model_dump()
    doc["timestamp"] = datetime.utcnow()
    res = logs.insert_one(doc)
    return {"id": str(res.inserted_id)}

@router.get("/logs")
def list_logs(limit: int = 50, skip: int = 0, modulo: str | None = None, accion: str | None = None, crit: str | None = None):
    q = {}
    if modulo: q["modulo"] = modulo
    if accion: q["accion"] = accion
    if crit: q["nivel_criticidad"] = crit
    cur = logs.find(q).skip(skip).limit(limit).sort("timestamp", -1)
    out = []
    for x in cur:
        x["id"] = str(x["_id"]); x.pop("_id", None)
        out.append(x)
    return out
