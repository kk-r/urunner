from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from db.session import get_db

from .service import user_service
from api.deps import get_admin_user
from schemas.user import UserCreate, User

router = APIRouter()

# Document


@router.get('/user/{id}', response_model=User, tags=['user'])
def user_get(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_admin_user)
):
    return user_service.get(db, id)


@router.post('/user', response_model=User, status_code=201, tags=['user'])
def user_create(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create(db, obj_in=user)

