from fastapi import FastAPI
from routers.user import router as user_router
from routers.prodructos import router as productos_router
from fastapi.staticfiles import StaticFiles
from routers.auth import router as auth_router

app = FastAPI()  # Inicializa la aplicación/contexto

#router 
app.include_router(user_router) #asociamos las rutas de usuario
app.include_router(productos_router) #asociamos las rutas de productos
app.include_router(auth_router)  # asociamos las rutas de autenticación
app.mount("/static", StaticFiles(directory="static"), name="static") 



#iniciar servidor uvicorn main:app --reload
# Esto iniciará el servidor en http://