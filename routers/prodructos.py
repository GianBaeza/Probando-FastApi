from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class productos(BaseModel):
    id: int
    name: str
    gmail: str | None = None
    beca: bool | None = None


listaProductos = [
    productos(id=1, name="John Doe", gmail="gola soy el mail"),
    productos(id=2, name="Jane Smith", gmail="jane.smith@example.com", beca=True),
    productos(
        id=3, name="Alice Johnson", gmail="alice.johnson@example.com", beca=False
    ),
]


# para inicial la apliacion ahora seria uvicorn user:app --reload utiliza el nombre del archivo
@router.get("/productos")
async def ListproductosJson():
    return listaProductos
