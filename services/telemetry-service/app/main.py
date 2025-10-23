from fastapi import FastAPI
from app.routes import telemetry, devices

app = FastAPI(title="Telemetry Service", version="1.0.0")
app.include_router(telemetry.router)
app.include_router(devices.router)
