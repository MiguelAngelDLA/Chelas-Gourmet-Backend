from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

class OrderCreate(BaseModel):
    deliveryAddress: str
    paymentToken: str

class OrderHistoryItem(BaseModel):
    orderId: uuid.UUID
    date: datetime
    total: float
    status: str

    class Config:
        from_attributes = True
        fields = {'orderId': 'id', 'date': 'created_at'} 

class OrderResponse(BaseModel):
    orderId: uuid.UUID
    status: str
    total: float
    estimatedDeliveryTime: str = "30-45 minutos" 

    class Config:
        from_attributes = True
        fields = {'orderId': 'id'} 
