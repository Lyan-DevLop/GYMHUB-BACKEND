from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Rol(SQLModel, table=True):
    """Tabla de roles."""
    __tablename__ = "roles"

    rol_id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str


class Usuario(SQLModel, table=True):
    """Tabla de usuarios."""
    __tablename__ = "usuarios"

    usuario_id: Optional[int] = Field(default=None, primary_key=True)
    nombre_usuario: str
    correo: str
    contrasena: str
    rol_id: int = Field(foreign_key="roles.rol_id")


class Servicio(SQLModel, table=True):
    """Tabla de servicios ofrecidos."""
    __tablename__ = "servicios"

    servicio_id: Optional[int] = Field(default=None, primary_key=True)
    nombre_servicio: str
    usuario_id: int = Field(foreign_key="usuarios.usuario_id")
    duracion: str
    cupos: int
    descripcion: str


class Estado(SQLModel, table=True):
    """Tabla de estados de reserva."""
    __tablename__ = "estado"

    estado_id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str


class Reserva(SQLModel, table=True):
    """Tabla de reservas."""
    __tablename__ = "reservas"

    reserva_id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.usuario_id")
    servicio_id: int = Field(foreign_key="servicios.servicio_id")
    estado_id: int = Field(foreign_key="estado.estado_id")
    fecha_reserva: datetime
