from fastapi import APIRouter, Depends, HTTPException
from typing import List
from itertools import count

from .auth import get_current_user, require_role
from .models import ItemIn, Item


router: APIRouter = APIRouter()

items_db: List[Item] = []
item_id_counter = count(1)


def create_item_in_db(item_in: ItemIn) -> Item:
    new_item: Item = Item(id=next(item_id_counter), **item_in.dict())
    items_db.append(new_item)
    return new_item


def delete_item_from_db(item_id: int) -> Item:
    for i, item in enumerate(items_db):
        if item.id == item_id:
            return items_db.pop(i)
    raise HTTPException(status_code=404, detail="Item not found")


def list_items_from_db() -> List[Item]:
    return items_db


@router.get("/")
async def root() -> dict:
    return {"message": "FastAPI is running"}


@router.get("/items", response_model=List[Item])
async def read_items(user=Depends(get_current_user)) -> List[Item]:
    return list_items_from_db()


@router.post("/items", response_model=Item)
async def create_item(item: ItemIn, user=Depends(require_role("admin"))) -> Item:
    return create_item_in_db(item)


@router.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int, user=Depends(require_role("admin"))) -> Item:
    return delete_item_from_db(item_id)
