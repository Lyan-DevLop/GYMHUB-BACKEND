from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ---------- ROLES ----------
class RolCreate(BaseModel):
    nombre: str


class RolRead(RolCreate):
    rol_id: int


# ---------- USUARIOS ----------
class UsuarioCreate(BaseModel):
    nombre_usuario: str
    correo: EmailStr
    contrasena: str
    rol_id: int


class UsuarioRead(UsuarioCreate):
    usuario_id: int


class UsuarioUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    correo: Optional[EmailStr] = None
    contrasena: Optional[str] = None
    rol_id: Optional[int] = None


# ---------- SERVICIOS ----------
class ServicioCreate(BaseModel):
    nombre_servicio: str
    usuario_id: int
    duracion: str
    cupos: int
    descripcion: str


class ServicioRead(ServicioCreate):
    servicio_id: int


class ServicioUpdate(BaseModel):
    nombre_servicio: Optional[str] = None
    usuario_id: Optional[int] = None
    duracion: Optional[str] = None
    cupos: Optional[int] = None
    descripcion: Optional[str] = None


# ---------- ESTADO ----------
class EstadoCreate(BaseModel):
    nombre: str


class EstadoRead(EstadoCreate):
    estado_id: int


# ---------- RESERVAS ----------
class ReservaCreate(BaseModel):
    usuario_id: int
    servicio_id: int
    estado_id: int
    fecha_reserva: datetime


class ReservaRead(ReservaCreate):
    reserva_id: int


class ReservaUpdate(BaseModel):
    usuario_id: Optional[int] = None
    servicio_id: Optional[int] = None
    estado_id: Optional[int] = None
    fecha_reserva: Optional[datetime] = None
