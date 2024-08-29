from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status
)
from pydantic import BaseModel

from users.schemas import UserSchema

from auth import utils as auth_utils


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


jwt_router = APIRouter(prefix='/jwt', tags=['JWT'])


john = UserSchema(
    username="John",
    password=auth_utils.hash_password('12345'),
    email='john@example.com'
)

sam = UserSchema(
    username="Sam",
    password=auth_utils.hash_password('qwerty'),
)


users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam
}


def validate_auth_user(
        username: str = Form(),
        password: str = Form()
):
    unauth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password'
    )
    if not (user := users_db.get(username)):
        raise unauth_exception

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauth_exception

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Inactive user'
        )

    raise user


@jwt_router.post('/login/', response_model=TokenInfo)
def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user)
):
    jwt_payload = {
        'sub': user.username,
        'username': user.username,
        'email': user.email
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )