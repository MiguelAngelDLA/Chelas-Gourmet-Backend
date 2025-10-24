from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import uuid
from .. import models, schemas

def get_active_cart_by_client_id(db: Session, client_id: uuid.UUID):
    return db.query(models.Cart).filter(
        models.Cart.client_id == client_id,
        models.Cart.status == "active"
    ).first()

def get_or_create_active_cart(db: Session, client_id: uuid.UUID):
    cart = get_active_cart_by_client_id(db, client_id)
    if not cart:
        cart = models.Cart(client_id=client_id, status="active")
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def add_item_to_cart(db: Session, cart: models.Cart, item_create: schemas.CartItemCreate):
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.item_id == item_create.itemId
    ).first()
    
    if existing_item:
        existing_item.quantity += item_create.quantity
    else:
        db_item = models.CartItem(
            cart_id=cart.id,
            item_id=item_create.itemId,
            quantity=item_create.quantity
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(cart)
    return cart