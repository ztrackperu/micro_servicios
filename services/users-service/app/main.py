from fastapi import FastAPI
from app.routes import auth, users

app = FastAPI(title="Users Service", version="1.0.0")
app.include_router(auth.router)
app.include_router(users.router)
