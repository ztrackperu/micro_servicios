from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

Crit = Literal["LOW","MEDIUM","HIGH","CRITICAL"]

class AuditLogIn(BaseModel):
    user_email: Optional[str] = None
    user_rol: Optional[str] = None
    accion: str
    modulo: str
    entidad_tipo: Optional[str] = None
    entidad_id: Optional[str] = None
    descripcion: Optional[str] = None
    nivel_criticidad: Crit = "LOW"
    context: Optional[dict] = None

class AuditLogOut(AuditLogIn):
    id: str
    timestamp: datetime
