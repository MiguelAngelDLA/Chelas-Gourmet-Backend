from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud, models
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/cart",
    tags=["Client - Cart"]
)

@router.get("", response_model=schemas.Cart)
def get_user_cart(
    db: Session = Depends(get_db),
    current_user: models.Client = Depends(get_current_user)
):
    cart = crud.crud_cart.get_or_create_active_cart(db, client_id=current_user.id)
    
    cart_items_response = []
    subtotal = 0.0
    
    for item in cart.items:
        if item.item: 
            cart_items_response.append(schemas.CartItem(
                cartItemId=item.id,
                itemId=item.item.id,
                name=item.item.name,
                quantity=item.quantity,
                unitPrice=item.item.price
            ))
            subtotal += item.item.price * item.quantity
            
    return schemas.Cart(items=cart_items_response, subtotal=subtotal)


@router.post("/items", response_model=schemas.Cart)
def add_item_to_user_cart(
    item_in: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: models.Client = Depends(get_current_user)
):
    """
    Añadir un artículo al carrito del usuario autenticado.
    """
    item_db = crud.crud_menu.get_item_by_id(db, item_id=str(item_in.itemId))
    if not item_db or not item_db.available:
        raise HTTPException(status_code=404, detail="Item not found or unavailable")

    cart = crud.crud_cart.get_or_create_active_cart(db, client_id=current_user.id)
    
    crud.crud_cart.add_item_to_cart(db, cart=cart, item_create=item_in)
    
    return get_user_cart(db, current_user)