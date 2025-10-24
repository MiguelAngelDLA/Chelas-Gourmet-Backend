from sqlalchemy.orm import Session
from sqlalchemy import desc # Para ordenar
import uuid
from .. import models, schemas, crud

def create_order_from_cart(
    db: Session, 
    cart: models.Cart, 
    order_data: schemas.OrderCreate
) -> models.Order:
    
    if not cart.items:
        raise ValueError("El carrito está vacío") 

    total = 0.0
    for cart_item in cart.items:
        total += cart_item.item.price * cart_item.quantity

    db_order = models.Order(
        client_id=cart.client_id,
        status="Pedido Recibido",
        total=total,
        delivery_address=order_data.deliveryAddress
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order) 

    for cart_item in cart.items:
        db_order_item = models.OrderItem(
            order_id=db_order.id,
            item_id=cart_item.item_id,
            quantity=cart_item.quantity,
            price_at_order=cart_item.item.price 
        )
        db.add(db_order_item)
    
    for cart_item in cart.items:
        db.delete(cart_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders_by_client_id(db: Session, client_id: uuid.UUID) -> List[models.Order]:
    return db.query(models.Order).filter(
        models.Order.client_id == client_id
    ).order_by(desc(models.Order.created_at)).all()
