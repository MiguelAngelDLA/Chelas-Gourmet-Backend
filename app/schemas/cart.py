from pydantic import BaseModel
from typing import List, Optional
import uuid

class CartItem(BaseModel):
    cartItemId: uuid.UUID 
    itemId: uuid.UUID
    name: str
    quantity: int
    unitPrice: float
    customizations: List = []

    class Config:
        from_attributes = True
        fields = {'cartItemId': 'id'} 

class CartItemCreate(BaseModel):
    itemId: uuid.UUID
    quantity: int = 1
    customizations: List = []

class Cart(BaseModel):
    items: List[CartItem]
    subtotal: float

    class Config:
        from_attributes = True