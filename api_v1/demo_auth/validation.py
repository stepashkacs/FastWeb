from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from api_v1.demo_auth.helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from auth import utils as auth_utils
from users.schemas import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/demo_auth/jwt/login/")
john = UserSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@example.com",
)
sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("secret"),
)
users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


def validate_token_type(
        payload: dict,
        token_type: str
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'invalid token type {current_token_type} != {token_type}'
    )


def get_user_by_token_sub(
        payload: dict
) -> UserSchema:
    username: str | None = payload.get('sub')
    if not (user := users_db.get(username)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (user not found)"
        )
    return user


def get_current_token_payload(
        # credentials: HTTPBasicCredentials = Depends(http_bearer)
        token: str = Depends(oauth2_scheme)
) -> UserSchema:
    # token = credentials.credentials
    try:

        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'invalid token error, {exception}'
        )
    return payload


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type
    def __call__(self,
            payload: dict = Depends(get_current_token_payload)
    ):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)

