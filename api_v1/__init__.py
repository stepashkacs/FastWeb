from fastapi import APIRouter

from .products.views import router_apiv1
from .demo_auth import demo_auth_router
from .demo_auth.demo_jwt_auth import jwt_router

demo_auth_router.include_router(jwt_router)
api_router = APIRouter()
api_router.include_router(demo_auth_router)
api_router.include_router(router=router_apiv1, prefix='/products')