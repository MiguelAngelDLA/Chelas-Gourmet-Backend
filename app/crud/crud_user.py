from sqlalchemy.orm import Session
import uuid
from .. import models, schemas, security

def get_client_by_email(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()

def get_client_by_auth_id(db: Session, auth_id: uuid.UUID):
    return db.query(models.Client).filter(models.Client.auth_id == auth_id).first()

def create_client(db: Session, user: schemas.UserCreate, auth_id: uuid.UUID):
    
    db_user = models.Client(
        auth_id=auth_id,
        email=user.email,
        name=user.name,
        role="client" 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user