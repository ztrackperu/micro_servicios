from fastapi import FastAPI, Request
import httpx
from app.core.config import settings

app = FastAPI(title="Gateway API", version="1.0.0")

# Rutas de proxy mínimas (se pueden ampliar por grupo)
@app.api_route("/api/auth/{path:path}", methods=["GET","POST","PUT","PATCH","DELETE"])
async def proxy_auth(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{settings.USERS_BASE_URL}/api/auth/{path}"
        req = request.scope
        body = await request.body()
        resp = await client.request(request.method, url, headers=dict(request.headers), content=body)
    return app.response_class(content=resp.content, status_code=resp.status_code, headers=resp.headers)

@app.api_route("/api/users/{path:path}", methods=["GET","POST","PUT","PATCH","DELETE"])
async def proxy_users(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{settings.USERS_BASE_URL}/api/users/{path}"
        body = await request.body()
        resp = await client.request(request.method, url, headers=dict(request.headers), content=body)
    return app.response_class(content=resp.content, status_code=resp.status_code, headers=resp.headers)

@app.api_route("/api/telemetry/{path:path}", methods=["GET","POST"])
async def proxy_telemetry(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{settings.TELEMETRY_BASE_URL}/api/telemetry/{path}"
        body = await request.body()
        resp = await client.request(request.method, url, headers=dict(request.headers), content=body)
    return app.response_class(content=resp.content, status_code=resp.status_code, headers=resp.headers)

@app.api_route("/api/devices/{path:path}", methods=["GET"])
async def proxy_devices(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{settings.TELEMETRY_BASE_URL}/api/devices/{path}"
        body = await request.body()
        resp = await client.request(request.method, url, headers=dict(request.headers), content=body)
    return app.response_class(content=resp.content, status_code=resp.status_code, headers=resp.headers)
