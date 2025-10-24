from pydantic import BaseModel
import uuid

class MenuCategory(BaseModel):
    id: uuid.UUID
    name: str 

    class Config:
        from_attributes = True
        fields = {'name': 'title'}