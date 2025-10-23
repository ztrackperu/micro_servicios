from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

Role = Literal["ADMIN", "MANAGER", "OPERATOR", "CLIENT"]

class UserBase(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str
    rol: Role = "CLIENT"
    empresa_id: Optional[str] = None
    activo: bool = True

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserOut(UserBase):
    id: str
    created_at: datetime

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    rol: Optional[Role] = None
    empresa_id: Optional[str] = None
    activo: Optional[bool] = None

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginIn(BaseModel):
    email: EmailStr
    password: str
