from fastapi import APIRouter, HTTPException
from models.models_auth import  Login,UserInDB,User



router = APIRouter(prefix="/login", tags=["auth"])
listaUsuarios = [
      UserInDB(
            username="admin",
            email="admin@example.com",
            hashed_password="123",
            direccion=None,
            telefono=None,
            fecha_nacimiento=None,
            genero=None,
            estado_civil=None
      ),
      UserInDB(
            username="user",
            email="user@example.com",
            hashed_password="123",
            direccion=None,
            telefono=None,
            fecha_nacimiento=None,
            genero=None,
            estado_civil=None
      ),
]


@router.get("/usuarios", status_code=200)
async def getUsers():
      return listaUsuarios
      
      
    
@router.post("/iniciarSession", status_code=200)
async def login(data: Login):
      
      if not data.user or not data.password:
            raise HTTPException(status_code=400, detail="Usuario y contraseña son requeridos")
      existe_user = next((user for user in listaUsuarios if user.username == data.user), None)
      
      if not existe_user:
            raise HTTPException(status_code=404, detail="Usuario incorrecto")
      if existe_user.hashed_password != data.password:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
      return {"message": "Inicio de sesión exitoso", "user": existe_user.username}
      
      
    
@router.get("/search", status_code=200)
async def searchUser(username: str):
      user = next((user for user in listaUsuarios if user.username == username), None)
      if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
      return User(  #retornamos el usuario sin expóner la password al front por que no es necesario
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            disabled=user.disabled
      )
      
