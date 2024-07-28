from fastapi import FastAPI
import uvicorn
from pydantic import EmailStr, BaseModel
from items_views import items_router
app = FastAPI()
app.include_router(items_router)

class CreateUser(BaseModel):
    email: EmailStr

@app.get('/')
def hello_index():
    return {
        "message": "Hello index,"
    }


@app.post('/user/')
def create_user(user: CreateUser):
    return {
        'message': 'succes',
        'email': user.email,
    }


@app.get('/hello/')
def hello(name: str = 'World'):
    name = name.strip().title()
    return {'message': f'Hello {name}'}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)