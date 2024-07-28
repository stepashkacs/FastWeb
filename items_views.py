from fastapi import APIRouter, Path
from typing import Annotated

items_router = APIRouter(tags = ['Items'], prefix = '/items')


@items_router.get('/')
def list_items():
    return [
        'Item1',
        'Item2',
        'Item3',
    ]

@items_router.get('/{item_id}/')
def get_item_by_id(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {
        'item': {
            'id': item_id,
        }
    }