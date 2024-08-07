from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import Product, ProductCreate, ProductUpdate, ProductPartial
from core.models import db_helper
from .dependencies import product_by_id


router_apiv1 = APIRouter(tags=['Products'])


@router_apiv1.get('/', response_model=list[Product])
async def get_products(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_products(session=session)


@router_apiv1.post('/', response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
        product_in: ProductCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(session=session, product_in=product_in)


@router_apiv1.get('/{product_id}/', response_model=Product)
async def get_product(
    product = Depends(product_by_id),
):
    return product



@router_apiv1.put('/{product_id}/')
async def update_product(
        product_update: ProductUpdate,
        product = Depends(product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> Product:
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update
    )


@router_apiv1.patch('/{product_id}/')
async def update_product(
        product_update: ProductPartial,
        product = Depends(product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> Product:
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True
    )


@router_apiv1.delete('/{product_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> None:
    await crud.delete_product(
        session=session,
        product=product
    )