from fastapi import FastAPI
from ml_models import ml_router
from admin import admin_route
from auth import auth_router
from starlette.middleware.cors import CORSMiddleware
from constants import *

import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(auth_router.router, prefix='/api/auth', tags=['auth'])
app.include_router(ml_router.router, prefix='/api/data', tags=['data'])
app.include_router(admin_route.router, prefix='/api/admin', tags=['admin'])


@app.get('/')
def read_root():
    return {'Welcome to FastAPI': 'IUE PROJECT'}

if __name__ == '__main__':
    uvicorn.run(app,host=HOST,port=int(PORT))