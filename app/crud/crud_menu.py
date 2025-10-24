from sqlalchemy.orm import Session
from typing import Optional
from .. import models 

def get_public_categories(db: Session):
    return db.query(models.Menu).filter(models.Menu.is_public == True).all()

def get_items(db: Session, category_id: Optional[str], search_term: Optional[str]):

    query = db.query(models.Item).join(models.Menu).filter(
        models.Menu.is_public == True,
        models.Item.available == True
    )
    
    if category_id:
        query = query.filter(models.Item.menu_id == category_id)
        
    if search_term:
        query = query.filter(models.Item.name.ilike(f"%{search_term}%"))
        
    return query.all()

def get_item_by_id(db: Session, item_id: str):
    
    return db.query(models.Item).filter(models.Item.id == item_id).first()
