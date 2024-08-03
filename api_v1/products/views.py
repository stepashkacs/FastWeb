from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import Product, ProductCreate
from core.models import db_helper

router_apiv1 = APIRouter(tags=['Products'])

@router_apiv1.get('/', response_model=list[Product])
async def get_products(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_products(session=session)

@router_apiv1.post('/', response_model=Product)
async def create_product(
        product_in: ProductCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(session=session, product_in=product_in)


@router_apiv1.get('/{product_id}/', response_model=Product)
async def get_product(
        product_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    product = await crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Product {product_id} not found'
    )

