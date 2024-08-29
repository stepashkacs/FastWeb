from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status
)
from pydantic import BaseModel
from fastapi.security import HTTPBearer

from api_v1.demo_auth.helpers import create_access_token, create_refresh_token
from api_v1.demo_auth.validation import users_db, get_current_token_payload, get_current_auth_user, get_current_auth_user_for_refresh
from users.schemas import UserSchema

from auth import utils as auth_utils


http_bearer = HTTPBearer(auto_error=False)


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
    refresh_token: str | None = None


jwt_router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)]
)


def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password'
    )
    if not (user := users_db.get(username)):
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Inactive user'
        )

    return user


@jwt_router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


def get_auth_user(
    user: UserSchema = Depends(get_current_auth_user)
):
    if user.active:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Inactive user'
        )


@jwt_router.post(
    '/refresh/',
    response_model=TokenInfo,
    response_model_exclude_none=True
)


def auth_refresh_jwt(
        user: UserSchema = Depends(get_current_auth_user_for_refresh)
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


@jwt_router.get("/users/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_auth_user)
):
    iat = payload.get('iat')
    return {
        'username': user.username,
        'email': user.email,
        'logged_in_at': iat
    }