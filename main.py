from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select, Session
from typing import List
#import psycopg2

from database import get_session, engine
import models
import schemas


app = FastAPI(title="GYMHUB API - FastAPI + Supabase")

# Si quieres crear tablas automáticamente (solo si NO existen en Supabase),
# descomenta la línea siguiente. Ten cuidado: si tu Supabase ya tiene la estructura, NO la uses.
# from sqlmodel import SQLModel
# SQLModel.metadata.create_all(engine)


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
        contraseña=payload.contraseña,
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
@app.get("/servicios", response_model=List[schemas.ServicioRead])
def get_servicios(session: Session = Depends(get_session)):
    return session.exec(select(models.Servicio)).all()


@app.get("/servicios/{servicio_id}", response_model=schemas.ServicioRead)
def get_servicio(servicio_id: int, session: Session = Depends(get_session)):
    servicio = session.get(models.Servicio, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


@app.post("/servicios", response_model=schemas.ServicioRead, status_code=status.HTTP_201_CREATED)
def create_servicio(payload: schemas.ServicioCreate, session: Session = Depends(get_session)):
    servicio = models.Servicio(**payload.dict())
    session.add(servicio)
    session.commit()
    session.refresh(servicio)
    return servicio


@app.patch("/servicios/{servicio_id}", response_model=schemas.ServicioRead)
def update_servicio(servicio_id: int, payload: schemas.ServicioUpdate, session: Session = Depends(get_session)):
    servicio = session.get(models.Servicio, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    obj_data = payload.dict(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(servicio, key, value)
    session.add(servicio)
    session.commit()
    session.refresh(servicio)
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
