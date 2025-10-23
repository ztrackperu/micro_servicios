from datetime import datetime, timezone
from dateutil import parser
from . import db
from pymongo import ASCENDING, DESCENDING

def ingest(payload: dict):
    # Campos mínimos
    if "imei" not in payload: raise ValueError("imei requerido")
    device_imei = str(payload["imei"])
    ts = payload.get("timestamp")
    timestamp = parser.isoparse(ts) if ts else datetime.now(tz=timezone.utc)

    # Insertar en G_datos_YYYY_MM
    col_name = db.month_coll("G_datos", timestamp)
    col = db.db[col_name]
    doc = {**payload, "timestamp": timestamp}
    res = col.insert_one(doc)

    # Índices base (idempotente)
    col.create_index([("imei", ASCENDING), ("timestamp", DESCENDING)])
    col.create_index([("timestamp", DESCENDING)])

    # Upsert en G_dispositivos_YYYY_MM
    dcol_name = db.month_coll("G_dispositivos", timestamp)
    dcol = db.db[dcol_name]
    last_data = {k:v for k,v in payload.items() if k not in ("_id",)}
    dcol.update_one(
        {"imei": device_imei},
        {
            "$set": {
                "imei": device_imei,
                "last_data": {
                    **last_data, "timestamp": timestamp
                },
                "status_linea": 1,
                "last_update": timestamp
            },
            "$setOnInsert": {
                "first_seen": timestamp,
                "total_messages": 0
            },
            "$inc": {"total_messages": 1}
        },
        upsert=True
    )
    dcol.create_index([("imei", ASCENDING)], unique=True)
    dcol.create_index([("status_linea", ASCENDING)])
    dcol.create_index([("last_update", DESCENDING)])

    return str(res.inserted_id)

def list_devices(month: str | None = None, status: int | None = None, limit: int = 50, skip: int = 0):
    # month formato YYYY_MM; si no, usa actual
    now = datetime.now(tz=timezone.utc)
    dcol_name = db.month_coll("G_dispositivos", now) if not month else f"G_dispositivos_{month}"
    dcol = db.db[dcol_name]
    filt = {}
    if status: filt["status_linea"] = status
    cur = dcol.find(filt).skip(skip).limit(limit).sort("last_update", -1)
    out = []
    for x in cur:
        x["id"] = str(x["_id"]); x.pop("_id", None)
        out.append(x)
    return out
