from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from db.session import get_db
from schemas.user import Login
from schemas.token import TokenUser
from core.security import create_access_token
from .controller import authenticate

router = APIRouter()


@router.post('/login/', response_model=TokenUser, tags=['auth'])
def login(user: Login, db: Session = Depends(get_db)) -> TokenUser:
    user_auth = authenticate(db, username=user.username, password=user.password, email=user.email)
    if not user_auth:
        credential_type = 'email' if user.email else 'username'
        raise HTTPException(
            status_code=400,
            detail=f'Incorrect {credential_type} or password'
        )
    return {
        'access_token': create_access_token(user_auth.username),
        'token_type': 'bearer',
        'role_id': user_auth.role.id if user_auth.role else None,
        'role_name': user_auth.role.name if user_auth.role else None
    }
