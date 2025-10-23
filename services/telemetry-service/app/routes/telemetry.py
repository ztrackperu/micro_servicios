from fastapi import APIRouter, HTTPException
from app.services.telemetry_service import ingest

router = APIRouter(prefix="/api/telemetry", tags=["Telemetry"])

@router.post("/ingest")
def ingest_telemetry(payload: dict):
    try:
        _id = ingest(payload)
        return {"inserted_id": _id}
    except ValueError as e:
        raise HTTPException(400, str(e))
