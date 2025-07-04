# Probando FastAPI

Este proyecto es una API construida con [FastAPI](https://fastapi.tiangolo.com/), un framework moderno y eficiente para crear servicios web con Python.

## ¿Qué es FastAPI?

FastAPI es un framework web que permite desarrollar APIs de manera rápida y sencilla aprovechando las anotaciones de tipo de Python. Proporciona:
- Excelente rendimiento comparable con NodeJS y Go.
- Documentación automática y exploración interactiva de la API (Swagger UI y ReDoc).
- Validación de datos automática basada en Pydantic.
- Soporte para OAuth2, autenticación, CORS, y más.

## Estructura del Proyecto

- `main.py`: Archivo principal que inicializa la aplicación y registra los routers.
- `routers/`: Carpeta donde se organizan las rutas por módulos (usuarios, productos, autenticación).
- `static/`: Carpeta pública para servir archivos estáticos (imágenes, CSS, JS, etc.).

## Cómo ejecutar el proyecto

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Inicia el servidor de desarrollo:
   ```bash
   uvicorn main:app --reload
   ```
   El servidor estará disponible en [http://localhost:8000](http://localhost:8000).

3. Accede a la documentación interactiva generada automáticamente en:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Buenas Prácticas

- Mantén los routers y la lógica separados en módulos.
- Utiliza Pydantic para la validación de datos.
- Usa variables de entorno para configuraciones sensibles.
- Documenta las rutas y modelos.

---

> Proyecto hecho con ❤️ utilizando FastAPI.
