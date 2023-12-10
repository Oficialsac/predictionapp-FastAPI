from fastapi import FastAPI
from ml_models import ml_router
from admin import admin_route
from auth import auth_router
from starlette.middleware.cors import CORSMiddleware
from constants import *

import uvicorn

# Crea una instancia de FastAPI
app = FastAPI()

# Agrega middleware para permitir CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Incluye los routers de las diferentes partes de la aplicación
app.include_router(auth_router.router, prefix='/api/auth', tags=['auth'])
app.include_router(ml_router.router, prefix='/api/data', tags=['data'])
app.include_router(admin_route.router, prefix='/api/admin', tags=['admin'])

# Ruta de bienvenida
@app.get('/')
def read_root():
    return {'Welcome to FastAPI': 'IUE PROJECT'}

# Si el script es ejecutado directamente, inicia el servidor con Uvicorn
if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=int(PORT))
