from fastapi import FastAPI
import uvicorn
from items_views import items_router
from users.views import user_router
app = FastAPI()
app.include_router(items_router)
app.include_router(user_router)


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