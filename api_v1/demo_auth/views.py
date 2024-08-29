import secrets
import uuid
from time import time
from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from typing import Annotated, Any


demo_auth_router = APIRouter(tags=['Demo Auth'], prefix='/demo_auth')

security = HTTPBasic()


@demo_auth_router.get('/basic-auth/')
def demo_basic_auth_credentials(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        'message': 'HeLLo',
        'username': credentials.username,
        'password': credentials.password
    }


usernames_to_passwords = {
    'admin': 'admin',
    'anton': 'qwerty',
}


static_auth_token_to_username = {
    '79e114c9dbc33d09ac04096369w2a081': 'admin',
    'b8d3c4362d54f75edb5299060ef53e3': 'john',
}


def get_auth_user_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid Username or Password',
        headers={'WWW-Authenticate': 'Basic'}
    )
    correct_password = usernames_to_passwords.get(credentials.username)

    if correct_password is None:
        raise unauthed_exception

    if not secrets.compare_digest(
            credentials.password.encode('utf-8'),
            correct_password.encode('utf-8')
    ): #проверка паролей
        raise unauthed_exception

    else:
        return credentials.username


def get_username_by_static_auth_token(
        static_token: str = Header(alias='static-auth-token')
) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Token invalid'
    )


@demo_auth_router.get('/basic-auth-username/')
def demo_basic_auth_username(
        auth_username: str = Depends(get_auth_user_username)
):
    return {
        'message': f'HeLLo, {auth_username}',
        'username': auth_username,
    }


@demo_auth_router.get('/some-auth-header-auth/')
def demo_auth_http_header(
        username: str = Depends(get_username_by_static_auth_token)
):
    return {
        'message': f'HeLLo, {username}',
        'username': username,
    }


COOKIES: dict[str, dict[str, Any]] = {}
COOKIES_SESSION_ID_KEY = 'web-app-session-id'


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(
        session_id: str = Cookie(alias=COOKIES_SESSION_ID_KEY)
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='not authentificated',
        )

    return COOKIES[session_id]


@demo_auth_router.post("/login-cookie/")
def demo_auth_login_set_cookie(
    response: Response,
    auth_username: str = Depends(get_auth_user_username),
    username: str = Depends(get_username_by_static_auth_token),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        # "username": username,
        "username": auth_username,
        "login_at": int(time()),
    }
    response.set_cookie(COOKIES_SESSION_ID_KEY, session_id)
    return {"result": "ok"}


@demo_auth_router.get("/check-cookie/")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "message": f"Hello, {username}!",
        **user_session_data,
    }


@demo_auth_router.get("/logout-cookie/")
def demo_auth_logout_cookie(
    response: Response,
    user_session_data: dict = Depends(get_session_data),
    session_id: str = Cookie(alias=COOKIES_SESSION_ID_KEY)
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIES_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {
        "message": f"Bye, {username}!",
        **user_session_data,
    }