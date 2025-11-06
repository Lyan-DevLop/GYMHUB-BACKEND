from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select, Session
from typing import List

from database import get_session
import models
import schemas
import re
from datetime import timedelta

from fastapi import FastAPI, Request, Response
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="GYMHUB API - FastAPI + Supabase")


app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],       # permite estos orígenes
    allow_credentials=False,
    allow_methods=["*"],         # GET, POST, PUT, DELETE
    allow_headers=["*"],         # headers personalizados
)


# Responder a peticiones OPTIONS
@app.options("/{rest_of_path:path}")
async def options_handler(rest_of_path: str):
    return JSONResponse(status_code=200)

# ---------- ROLES ----------
@app.get("/roles", response_model=List[schemas.RolRead])
def get_roles(session: Session = Depends(get_session)):
    roles = session.exec(select(models.Rol)).all()
    return roles


@app.get("/roles/{rol_id}", response_model=schemas.RolRead)
def get_rol(rol_id: int, session: Session = Depends(get_session)):
    rol = session.get(models.Rol, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol


@app.post("/roles", response_model=schemas.RolRead, status_code=status.HTTP_201_CREATED)
def create_rol(payload: schemas.RolCreate, session: Session = Depends(get_session)):
    rol = models.Rol(nombre=payload.nombre)
    session.add(rol)
    session.commit()
    session.refresh(rol)
    return rol


@app.put("/roles/{rol_id}", response_model=schemas.RolRead)
def update_rol(rol_id: int, payload: schemas.RolCreate, session: Session = Depends(get_session)):
    rol = session.get(models.Rol, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    rol.nombre = payload.nombre
    session.add(rol)
    session.commit()
    session.refresh(rol)
    return rol


@app.delete("/roles/{rol_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rol(rol_id: int, session: Session = Depends(get_session)):
    rol = session.get(models.Rol, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    session.delete(rol)
    session.commit()
    return None


# ---------- USUARIOS ----------
@app.get("/usuarios", response_model=List[schemas.UsuarioRead])
def get_usuarios(session: Session = Depends(get_session)):
    return session.exec(select(models.Usuario)).all()


@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioRead)
def get_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(models.Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@app.post("/usuarios", response_model=schemas.UsuarioRead, status_code=status.HTTP_201_CREATED)
def create_usuario(payload: schemas.UsuarioCreate, session: Session = Depends(get_session)):
    usuario = models.Usuario(
        nombre_usuario=payload.nombre_usuario,
        correo=payload.correo,
        contrasena=payload.contrasena,
        rol_id=payload.rol_id,
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@app.patch("/usuarios/{usuario_id}", response_model=schemas.UsuarioRead)
def update_usuario(usuario_id: int, payload: schemas.UsuarioUpdate, session: Session = Depends(get_session)):
    usuario = session.get(models.Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    obj_data = payload.dict(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(usuario, key, value)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(models.Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(usuario)
    session.commit()
    return None


# ---------- SERVICIOS ----------
def parse_duracion(texto: str) -> timedelta:
    horas = minutos = 0
    if match := re.search(r"(\d+)\s*h", texto):
        horas = int(match.group(1))
    if match := re.search(r"(\d+)\s*m", texto):
        minutos = int(match.group(1))
    return timedelta(hours=horas, minutes=minutos)


# 🔹 Función para convertir timedelta a texto (al devolver)
def format_duracion(valor) -> str:
    if isinstance(valor, timedelta):
        total_seconds = int(valor.total_seconds())
        horas, resto = divmod(total_seconds, 3600)
        minutos, _ = divmod(resto, 60)
        return f"{horas}h {minutos}m"
    return str(valor)


# -----------------------------
# 🟩 ENDPOINTS CRUD COMPLETOS
# -----------------------------

@app.get("/servicios", response_model=list[schemas.ServicioRead])
def get_servicios(session: Session = Depends(get_session)):
    servicios = session.exec(select(models.Servicio)).all()
    # Convertir timedelta → string
    for s in servicios:
        s.duracion = format_duracion(s.duracion)
    return servicios


@app.get("/servicios/{servicio_id}", response_model=schemas.ServicioRead)
def get_servicio(servicio_id: int, session: Session = Depends(get_session)):
    servicio = session.get(models.Servicio, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    servicio.duracion = format_duracion(servicio.duracion)
    return servicio


@app.post("/servicios", response_model=schemas.ServicioRead, status_code=status.HTTP_201_CREATED)
def create_servicio(payload: schemas.ServicioCreate, session: Session = Depends(get_session)):
    data = payload.dict()
    print("DEBUG PAYLOAD:", payload.dict())
    # Convertir texto a timedelta antes de guardar
    if "duracion" in data and isinstance(data["duracion"], str):
        data["duracion"] = parse_duracion(data["duracion"])

    servicio = models.Servicio(**data)
    session.add(servicio)
    session.commit()
    session.refresh(servicio)

    # Convertir a texto antes de devolver
    servicio.duracion = format_duracion(servicio.duracion)
    return servicio


@app.patch("/servicios/{servicio_id}", response_model=schemas.ServicioRead)
def update_servicio(servicio_id: int, payload: schemas.ServicioUpdate, session: Session = Depends(get_session)):
    servicio = session.get(models.Servicio, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    obj_data = payload.dict(exclude_unset=True)

    # Si viene duracion en texto, convertirla a timedelta
    if "duracion" in obj_data and isinstance(obj_data["duracion"], str):
        obj_data["duracion"] = parse_duracion(obj_data["duracion"])

    for key, value in obj_data.items():
        setattr(servicio, key, value)

    session.add(servicio)
    session.commit()
    session.refresh(servicio)

    servicio.duracion = format_duracion(servicio.duracion)
    return servicio


@app.delete("/servicios/{servicio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_servicio(servicio_id: int, session: Session = Depends(get_session)):
    servicio = session.get(models.Servicio, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    session.delete(servicio)
    session.commit()
    return None


# ---------- ESTADO ----------
@app.get("/estado", response_model=List[schemas.EstadoRead])
def get_estados(session: Session = Depends(get_session)):
    return session.exec(select(models.Estado)).all()


@app.get("/estado/{estado_id}", response_model=schemas.EstadoRead)
def get_estado(estado_id: int, session: Session = Depends(get_session)):
    estado = session.get(models.Estado, estado_id)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return estado


@app.post("/estado", response_model=schemas.EstadoRead, status_code=status.HTTP_201_CREATED)
def create_estado(payload: schemas.EstadoCreate, session: Session = Depends(get_session)):
    estado = models.Estado(nombre=payload.nombre)
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado


@app.put("/estado/{estado_id}", response_model=schemas.EstadoRead)
def update_estado(estado_id: int, payload: schemas.EstadoCreate, session: Session = Depends(get_session)):
    estado = session.get(models.Estado, estado_id)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    estado.nombre = payload.nombre
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado


@app.delete("/estado/{estado_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_estado(estado_id: int, session: Session = Depends(get_session)):
    estado = session.get(models.Estado, estado_id)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    session.delete(estado)
    session.commit()
    return None


# ---------- RESERVAS ----------
@app.get("/reservas", response_model=List[schemas.ReservaRead])
def get_reservas(session: Session = Depends(get_session)):
    return session.exec(select(models.Reserva)).all()


@app.get("/reservas/{reserva_id}", response_model=schemas.ReservaRead)
def get_reserva(reserva_id: int, session: Session = Depends(get_session)):
    reserva = session.get(models.Reserva, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva


@app.post("/reservas", response_model=schemas.ReservaRead, status_code=status.HTTP_201_CREATED)
def create_reserva(payload: schemas.ReservaCreate, session: Session = Depends(get_session)):
    reserva = models.Reserva(**payload.dict())
    session.add(reserva)
    session.commit()
    session.refresh(reserva)
    return reserva


@app.patch("/reservas/{reserva_id}", response_model=schemas.ReservaRead)
def update_reserva(reserva_id: int, payload: schemas.ReservaUpdate, session: Session = Depends(get_session)):
    reserva = session.get(models.Reserva, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    obj_data = payload.dict(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(reserva, key, value)
    session.add(reserva)
    session.commit()
    session.refresh(reserva)
    return reserva


@app.delete("/reservas/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reserva(reserva_id: int, session: Session = Depends(get_session)):
    reserva = session.get(models.Reserva, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    session.delete(reserva)
    session.commit()
    return None


@app.get("/reservas/usuario/{usuario_id}", response_model=List[schemas.ReservaRead])
def get_reservas_por_usuario(usuario_id: int, session: Session = Depends(get_session)):
    reservas = session.query(models.Reserva).filter(models.Reserva.usuario_id == usuario_id).all()
    if not reservas:
        raise HTTPException(status_code=404, detail="No se encontraron reservas para este usuario")
    return reservas
