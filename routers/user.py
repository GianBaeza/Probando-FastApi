from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any

router = APIRouter()


class User(BaseModel):
      id: int
      name: str
      gmail: str | None = None
      beca: bool | None = None

class Becario(User):
      universidad: str | None = None
      carrera: str | None = None

listaUsers = [
    User(id=1, name="John Doe", gmail="gola soy el mail"),
    User(id=2, name="Jane Smith", gmail="jane.smith@example.com", beca=True),
    User(id=3, name="Alice Johnson", gmail="alice.johnson@example.com", beca=False),
]


# para inicial la apliacion ahora seria uvicorn user:app --reload utiliza el nombre del archivo
@router.get("/users")
async def ListusersJson():
    return listaUsers


@router.get("/user/{id}")
async def userJson(id: int):
    user = next((user for user in listaUsers if user.id == id), None)
    if user is None:
        return {"error": "No se encontro el usuario"}
    return user


@router.post("/user/crearUsuario" ,status_code=201)
async def crearUsuario(user: User) -> dict[str, Any]:
    # Verificar si el usuario ya existe
    usuario_existente = next((u for u in listaUsers if u.id == user.id), None)
    if usuario_existente is not None:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    listaUsers.append(user)
    return {"message": "Usuario creado exitosamente", "user": user}


@router.put("/user/actualizarUsuario")
async def actualizarUsuario(user: User) -> dict[str, Any]:
    idUser = user.id
    usuario_existente = next((u for u in listaUsers if u.id == idUser), None)
    if usuario_existente is None:
        return {"error": "Usuario no encontrado"}
    else:
        # Actualizar el usuario existente
        usuario_existente.name = user.name
        usuario_existente.gmail = user.gmail
        return {
            "message": "Usuario actualizado exitosamente",
            "user": usuario_existente,
        }


@router.delete("/user/eliminar/{id}")
async def eliminarUsuario(id: int) -> dict[str, Any]:
    
    usuario_existente = next((u for u in listaUsers if u.id == id), None)
    if usuario_existente is None:
        return {"error": "Usuario no encontrado"}
    if usuario_existente.beca:
        return {"error": "No se puede eliminar un usuario con beca Activa"}
    listaUsers.remove(usuario_existente)
    return {"message": "Usuario eliminado exitosamente", "user": usuario_existente}
