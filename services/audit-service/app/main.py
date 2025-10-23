from fastapi import FastAPI
from app.routes import logs

app = FastAPI(title="Audit Service", version="1.0.0")
app.include_router(logs.router)
