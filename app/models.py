from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    name = Column(String)
    email = Column(String, unique=True)

class Menu(Base):
    __tablename__ = "menus"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    is_public = Column(Boolean, default=True)

class Item(Base):
    __tablename__ = "items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    available = Column(Boolean, default=True)