from pydantic import BaseModel


class User(BaseModel):
    username:str
    email: str
    full_name: str | None = None
    disabled: bool | None = None



class UserInDB(User):
    hashed_password: str
    direccion: str | None = None
    telefono: str | None = None
    fecha_nacimiento: str | None = None
    genero: str | None = None
    estado_civil: str | None = None
    
    
    
class Login(BaseModel):
    user:str
    password: str
