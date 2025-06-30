from typing import List, Optional
from routers.user import User  

def buscarUsuarioPorId(lista: List[User], id: int) -> Optional[User]:
      return next((user for user in lista if user.id == id), None)