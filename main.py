from typing import Annotated
from fastapi import FastAPI, Path
import uvicorn
from pydantic import EmailStr, BaseModel
app = FastAPI()

class CreateUser(BaseModel):
    email: EmailStr

@app.get('/')
def hello_index():
    return {
        "message": "Hello index,"
    }

@app.get('/items/')
def list_items():
    return [
        'Item1',
        'Item2',
        'Item3',
    ]

@app.get('/items/{item_id}/')
def get_item_by_id(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {
        'item': {
            'id': item_id,
        }
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