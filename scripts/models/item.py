# models/item.py
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    id: int
    name: str
    email: str

class ItemCreate(BaseModel):  # for POST request body
    name: str
    email: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ViewCart(BaseModel):
    pizza_ids: List[int]

class CalculateTotalItem(BaseModel):
    pizza_id: int
    quantity: int

class CalculateTotalRequest(BaseModel):
    items: List[CalculateTotalItem]