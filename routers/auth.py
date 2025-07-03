from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from models.models_auth import UserInDB, User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from utils.hash_pass import hash_Token

router = APIRouter(prefix="/auth", tags=["auth"])
listaUsuarios = {
    "admin": UserInDB(
        username="admin",
        email="admin@example.com",
        hashed_password="123",
        direccion=None,
        telefono=None,
        fecha_nacimiento=None,
        genero=None,
        estado_civil=None,
    ),
    "user": UserInDB(
        username="user",
        email="user@example.com",
        hashed_password="123",
        direccion=None,
        telefono=None,
        fecha_nacimiento=None,
        genero=None,
        estado_civil=None,
    ),
}

auth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def fake_decode_token(token: str):
    return listaUsuarios.get(
        token, None
    )  # simulamos una decodificación de token y retornamos el usuario si existe


async def current_user(token: str = Depends(auth2_scheme)):
    existe_user = await fake_decode_token(token)
    if not existe_user:
        raise HTTPException(
            status_code=404,
            detail="Credenciales de usuario no válidas",
        )
    return existe_user


@router.post("/login", status_code=200)
async def login(data: OAuth2PasswordRequestForm = Depends()):

    if not data.username or not data.password:
        raise HTTPException(
            status_code=400, detail="Usuario y contraseña son requeridos"
        )
    existe_user = listaUsuarios.get(data.username)

    if not existe_user:
        raise HTTPException(status_code=404, detail="Usuario incorrecto")
    if existe_user.hashed_password != data.password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    existe_user.hashed_password = hash_Token(existe_user.hashed_password)
    print(f"Token generado: {existe_user.hashed_password}")
    return {
        "message": "Inicio de sesión exitoso",
        "user": existe_user.username,
        "access_token": existe_user.hashed_password,
        "token_type": "bearer",
    }


@router.get("/usuarios", status_code=200)
async def getUsers(token: str = Depends(current_user)):
    return listaUsuarios


@router.get("/search", status_code=200)
async def searchUser(
    username: str,
    token: Annotated[str, Depends(current_user)],
):  # Annotated te permite asociar un parámetro con una dependencia o validador.
    # El endpoint no se ejecuta hasta que la dependencia se resuelve correctamente.
    # Si falla, FastAPI responde con un error antes de entrar a tu lógica.
    user = listaUsuarios.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return User(  # retornamos el usuario sin expóner la password al front por que no es necesario
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        disabled=user.disabled,
    )
