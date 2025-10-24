from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from .. import schemas, crud
from ..database import get_db

router = APIRouter(
    prefix="/menu",
    tags=["Client - Menu"]
)

@router.get("/categories", response_model=List[schemas.MenuCategory])
def get_menu_categories(db: Session = Depends(get_db)):
    categories = crud.crud_menu.get_public_categories(db)
    
    return [
        schemas.MenuCategory(id=cat.id, name=cat.title) for cat in categories
    ]

@router.get("/items", response_model=List[schemas.Item])
def get_menu_items(
    category: Optional[uuid.UUID] = Query(None, description="ID de la categoría (menu_id) para filtrar"),
    search: Optional[str] = Query(None, description="Término para buscar platillos por nombre"),
    db: Session = Depends(get_db)
):
    category_str = str(category) if category else None
    
    items = crud.crud_menu.get_items(db=db, category_id=category_str, search_term=search)
    
    return [
        schemas.Item(
            id=item.id,
            name=item.name,
            shortDescription=item.description, # Mapeo
            price=item.price
        ) for item in items
    ]

@router.get("/items/{itemId}", response_model=schemas.Item) 
def get_menu_item_detail(itemId: uuid.UUID, db: Session = Depends(get_db)):

    item_id_str = str(itemId)
    item = crud.crud_menu.get_item_by_id(db, item_id=item_id_str)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    return schemas.Item(
        id=item.id,
        name=item.name,
        shortDescription=item.description,
        price=item.price
    )
