from fastapi import FastAPI
from auth import router
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

app.include_router(router.router, prefix='/api/auth', tags=['auth'])


@app.get('/')
def read_root():
    return {'Welcome to FastAPI': 'IUE PROJECT'}

if __name__ == '__main__':
    uvicorn.run(app,host=HOST,port=int(PORT))