from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from models.auth import UserInDB, UserRegister
import os
from dotenv import load_dotenv
load_dotenv() # Cargar las variables de entorno desde el archivo .env


router = APIRouter(tags=["auth"]) # Agrupar las rutas de autenticación bajo el tag "auth"
oauth2 = OAuth2PasswordBearer(tokenUrl="login") # Configurar el esquema de seguridad OAuth2 para el inicio de sesión

Fake_DB: dict[str, UserInDB] = {}
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Contexto de encriptación para las contraseñas



ALGORITMO = os.getenv("ALGORITHM")  # Algoritmo de encriptación del JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)  # Tiempo de expiración del token en minutos


def get_password_hash(password: str) -> str:  # Hashea la contraseña usando bcrypt
    return pwd_context.hash(password)


def verificar_password(
    password: str, hashed_password: str
) -> bool:  # Verifica si la contraseña coincide con el hash
    return pwd_context.verify(password, hashed_password)


def usuario_autenticado(
    db: dict[str, UserInDB], username: str, password: str
):  # Verifica usuario y contraseña en la base de datos
    user = db.get(username)
    if not user:
        return False
    if not verificar_password(password, user.hashed_password):
        return False
    return True


async def get_current_user(
    token: str = Depends(oauth2),
):  # Obtiene el usuario actual a partir del token JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = Fake_DB.get(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
):  # Crea un JWT de acceso con expiración
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITMO)
    return encoded_jwt


@router.post("/registrar")
async def registrarUsuario(
    user: UserRegister,
):  # Registra un nuevo usuario en la base de datos falsa
    if not user.username or not user.email:
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario y el correo electrónico son obligatorios",
        )

    if user.username in Fake_DB:
        raise HTTPException(status_code=400, detail="Nombre de usuario existente")

    if user.email in [u.email for u in Fake_DB.values()]:
        raise HTTPException(status_code=400, detail="Correo electrónico ya registrado")

    usuario_en_db = UserInDB(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
    )

    Fake_DB[user.username] = usuario_en_db

    return {"mensaje": "Usuario registrado correctamente"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user: Annotated[OAuth2PasswordRequestForm, Depends()],
):  # Inicia sesión y retorna el token JWT si es exitoso
    usuario = user.username
    password = user.password

    user_existente = usuario_autenticado(Fake_DB, usuario, password)
    if not user_existente:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )  # Tiempo de expiración del token
    access_token = create_access_token(
        data={
            "sub": user.username,
            "exp": access_token_expires,
            "direccion": "carrera 123",
            "telefono": "1234567890",
        },
        expires_delta=access_token_expires,
    )
    return {"mensaje": "Inicio de sesión exitoso", "access_token": access_token}


@router.get("/all/users")
async def obtenerUsuarios(
    depe: Annotated[UserInDB, Depends(get_current_user)],
):  # Devuelve todos los usuarios registrados (requiere autenticación)
    return Fake_DB
