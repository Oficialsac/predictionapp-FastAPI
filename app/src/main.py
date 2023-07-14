from fastapi import FastAPI
from auth import router
import uvicorn

app = FastAPI()
app.include_router(router.router, prefix='/api/auth', tags=['auth'])

@app.get('/')
def read_root():
    return {'hello': 'world'}


if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8080)