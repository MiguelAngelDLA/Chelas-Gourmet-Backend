from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud, security, models
from ..database import get_db
from ..supabase_client import supabase 
from gotrue.errors import AuthApiError

router = APIRouter(
    prefix="/admin/auth",
    tags=["Admin - Auth"]
)

@router.post("/login", response_model=security.Token)
def login_admin_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    
    try:
        session_response = supabase.auth.sign_in_with_password({
            "email": form_data.username,
            "password": form_data.password
        })
        
        auth_id = session_response.user.id
        user_profile = crud.crud_user.get_client_by_auth_id(db, auth_id=auth_id)
        
        if not user_profile or user_profile.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado. El usuario no es un administrador."
            )
        
        return {
            "access_token": session_response.session.access_token,
            "token_type": "bearer"
        }
        
    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Email o contraseña incorrectos: {e.message}",
            headers={"WWW-Authenticate": "Bearer"},
        )
