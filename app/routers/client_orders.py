from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud, models
from ..database import get_db
from ..dependencies import get_current_user 

router = APIRouter(
    prefix="/orders",
    tags=["Client - Orders"]
)

@router.post("", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_new_order(
    order_in: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.Client = Depends(get_current_user)
):
    cart = crud.crud_cart.get_active_cart_by_client_id(db, client_id=current_user.id)
    
    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay items en el carrito para procesar"
        )
    
    try:
        db_order = crud.crud_order.create_order_from_cart(
            db=db, cart=cart, order_data=order_in
        )
        return schemas.OrderResponse(
            orderId=db_order.id,
            status=db_order.status,
            total=db_order.total
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No se pudo procesar el pedido: {e}"
        )


@router.get("", response_model=List[schemas.OrderHistoryItem])
def get_order_history(
    db: Session = Depends(get_db),
    current_user: models.Client = Depends(get_current_user)
):
    
    orders = crud.crud_order.get_orders_by_client_id(db, client_id=current_user.id)
    
    return [
        schemas.OrderHistoryItem(
            orderId=order.id,
            date=order.created_at,
            total=order.total,
            status=order.status
        ) for order in orders
    ]
