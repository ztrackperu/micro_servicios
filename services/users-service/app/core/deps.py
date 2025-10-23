from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from .config import settings
from common.utils.jwt_manager import decode_token

bearer = HTTPBearer(auto_error=True)

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    token = creds.credentials
    try:
        payload = decode_token(token, settings.JWT_SECRET, [settings.JWT_ALG])
        return payload  # {"sub": email, "rol": "...", "uid": "..."}
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido") from e

def require_roles(*roles: str):
    def _dep(payload = Depends(get_current_user)):
        if payload.get("rol") not in roles:
            raise HTTPException(status_code=403, detail="Permisos insuficientes")
        return payload
    return _dep
