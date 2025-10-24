from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from gotrue.errors import AuthApiError

from .. import schemas, crud, security, models
from ..database import get_db
from ..supabase_client import supabase 

router = APIRouter(
    prefix="/auth",
    tags=["Client - Auth"]
)

@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_exists = crud.crud_user.get_client_by_email(db, email=user.email)
    if db_user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ya registrado. Por favor, use otro email."
        )
    
    try:
        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "name": user.name
                }
            }
        })
        
        auth_id = auth_response.user.id
        
        created_user = crud.crud_user.create_client(
            db=db, user=user, auth_id=auth_id
        )
        
        return {
            "message": "Usuario registrado exitosamente. Por favor, revise su email para la confirmación.",
            "userId": created_user.id
        }

    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error de autenticación: {e.message}"
        )

@router.post("/login", response_model=security.Token)
def login_for_access_token(
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
        
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario autenticado pero perfil no encontrado."
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