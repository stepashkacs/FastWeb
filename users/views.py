from fastapi import APIRouter
from users.schemas import CreateUser
from users import crud
user_router = APIRouter(tags=['Users'], prefix='/users')

@user_router.post('/')
def create_user(user: CreateUser):
    return crud.create_user(user_in=user)