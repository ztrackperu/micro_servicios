from fastapi import APIRouter, Depends, HTTPException, Query
from common.schemas.user_schema import UserOut, UserUpdate, UserCreate
from app.services.user_service import get_user, list_users, update_user, delete_user, create_user
from app.core.deps import require_roles, get_current_user

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/", response_model=list[UserOut])
def get_users(
    skip: int = 0, limit: int = 50,
    q: str | None = None, rol: str | None = None, activo: bool | None = None,
    _=Depends(require_roles("ADMIN","MANAGER"))
):
    return list_users(skip, limit, q, rol, activo)

@router.get("/me", response_model=UserOut)
def me(payload=Depends(get_current_user)):
    user = get_user(payload["uid"])
    if not user: raise HTTPException(404, "Usuario no encontrado")
    return user

@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: str, _=Depends(require_roles("ADMIN","MANAGER"))):
    user = get_user(user_id)
    if not user: raise HTTPException(404, "No existe")
    return user

@router.post("/", response_model=UserOut)
def create_user_admin(payload: UserCreate, _=Depends(require_roles("ADMIN"))):
    try:
        return create_user(
            email=payload.email,
            password=payload.password,
            nombre=payload.nombre,
            apellido=payload.apellido,
            rol=payload.rol,
            empresa_id=payload.empresa_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{user_id}", response_model=UserOut)
def patch_user(user_id: str, payload: UserUpdate, _=Depends(require_roles("ADMIN","MANAGER"))):
    updated = update_user(user_id, payload.model_dump(exclude_unset=True))
    if not updated: raise HTTPException(404, "No existe")
    return updated

@router.delete("/{user_id}")
def remove_user(user_id: str, _=Depends(require_roles("ADMIN"))):
    ok = delete_user(user_id)
    if not ok: raise HTTPException(404, "No existe")
    return {"deleted": True}
