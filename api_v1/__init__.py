from fastapi import APIRouter

from .products.views import router_apiv1

api_router = APIRouter()
api_router.include_router(router=router_apiv1, prefix='/products')