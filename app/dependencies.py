from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import uuid

from . import security, models, crud
from .database import get_db
from .crud import crud_user 
from . import security, models, crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(...)
    
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM],
            options={"verify_aud": False} 
        )
        
        auth_id_str: str = payload.get("sub")
        if auth_id_str is None:
            raise credentials_exception
        
        auth_id_uuid = uuid.UUID(auth_id_str)
        
    except (JWTError, ValueError):
        raise credentials_exception
    
    user = crud.crud_user.get_client_by_auth_id(db, auth_id=auth_id_uuid)
    
    if user is None:
        raise credentials_exception
        
    return user