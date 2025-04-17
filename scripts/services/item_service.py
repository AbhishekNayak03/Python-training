# services/item_service.py

from fastapi import APIRouter, Path, Body
from typing import List, Union
from scripts.models.item import Item, ItemCreate, LoginRequest, ViewCart
from scripts.handlers import item_handler

router = APIRouter()

@router.get("/users", response_model=Union[List[Item], dict])
def read_items():
    return item_handler.read_items_logic()

@router.post("/items", response_model=Item)
def create_item(item: ItemCreate):
    return item_handler.create_item_logic(item)

@router.delete("/items/{item_id}")
def delete_item(item_id: int = Path(..., title="The ID of the item to delete")):
    return item_handler.delete_item_logic(item_id)

@router.post("/login")
def login_user(request: LoginRequest):
    return item_handler.login_user_logic(request)

@router.get("/get_all_pizzas")
def get_all_pizzas():
    return item_handler.get_all_pizzas_logic()

@router.post("/view_cart")
def view_cart(request: ViewCart):
    return item_handler.view_cart_logic(request.dict())

