from fastapi import FastAPI
import uvicorn

from items_views import items_router
from users.views import user_router
from api_v1 import api_router

from contextlib import asynccontextmanager
from core.models import Base, db_helper

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(items_router)
app.include_router(user_router)
app.include_router(api_router)


@app.get('/')
def hello_index():
    return {
        "message": "Hello index,"
    }



@app.get('/hello/')
def hello(name: str = 'World'):
    name = name.strip().title()
    return {'message': f'Hello {name}'}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)