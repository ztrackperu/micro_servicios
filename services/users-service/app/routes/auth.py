from fastapi import APIRouter, HTTPException
from common.schemas.user_schema import LoginIn, TokenOut, UserCreate, UserOut
from app.services.user_service import authenticate, create_user
from common.utils.jwt_manager import create_access_token
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate):
    try:
        user = create_user(
            email=payload.email,
            password=payload.password,
            nombre=payload.nombre,
            apellido=payload.apellido,
            rol=payload.rol,
            empresa_id=payload.empresa_id
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn):
    user = authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token(
        data={"sub": user["email"], "rol": user["rol"], "uid": user["id"]},
        secret=settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
        expire_minutes=settings.JWT_EXPIRE_MIN
    )
    return {"access_token": token}
