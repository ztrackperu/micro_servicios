from fastapi import APIRouter, Query
from app.services.telemetry_service import list_devices

router = APIRouter(prefix="/api/devices", tags=["Devices"])

@router.get("/status")
def get_devices(status: int | None = Query(None), month: str | None = Query(None), skip: int = 0, limit: int = 50):
    return list_devices(month, status, limit, skip)
