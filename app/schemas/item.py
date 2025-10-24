from pydantic import BaseModel
from typing import Optional
import uuid

class Item(BaseModel):
    id: uuid.UUID
    name: str
    shortDescription: Optional[str] 
    price: float
    imageUrl: Optional[str] = None 

    class Config:
        from_attributes = True
        fields = {'shortDescription': 'description'}