from pydantic import BaseModel, EmailStr
import uuid

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    message: str
    userId: uuid.UUID

    class Config:
        from_attributes = True