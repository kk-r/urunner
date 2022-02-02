
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from core.role import ROLE
from fastapi import APIRouter, Depends

from db.session import get_db
from models.user import User
from models.role import Role
from models.jogging import Jogging as JoggingModel
from schemas.jogging import Jogging, JoggingComplete, JoggingCreate, JoggingUpdate, ListJoggings, JoggingInDbBase
from schemas.user import UserCreate

from .service import jogging_service
from api.deps import get_admin_user, get_current_user

router = APIRouter()

# Document


@router.post('/jogging', response_model=Jogging, status_code=201, tags=['jogging'])
def jogging_create(jog: JoggingCreate, db: Session = Depends(get_db), current_user: JoggingCreate = Depends(get_current_user)):
    return jogging_service.create(db, obj_in=jog, current_user=current_user)

    
@router.delete('/jogging/{id}', response_model=Jogging, tags=['jogging'])
def delete_jogging(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_current_user)
):
    jogging = jogging = db.query(JoggingModel).get(id)
    
    if not jogging:
        raise HTTPException(status_code=404, detail="resource not found")
    
    role = getattr(getattr(current_user, 'role'), 'name', None)
    
    if role == ROLE.BASIC.value and jogging.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Permission denied")
    
    jogging_user = jogging.user
    jogging_user_role = jogging_user.role
    
    if role == ROLE.MANAGER.value and (jogging_user.id != current_user.id and jogging_user_role.name in [ROLE.MANAGER.value, ROLE.ADMIN.value]):
        raise HTTPException(status_code=401, detail="Permission denied")
    
    return jogging_service.remove(db, id=id)


@router.put('/jogging/{id}', response_model=JoggingComplete, tags=['jogging'])
def update_jogging(
    id: int,
    jogg: JoggingUpdate,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_current_user)
):
    jogging = jogging = db.query(JoggingModel).get(id)
    
    if not jogging:
        raise HTTPException(status_code=404, detail="resource not found")
    
    role = getattr(getattr(current_user, 'role'), 'name', None)
    
    if role == ROLE.BASIC.value and jogging.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Permission denied")
    
    jogging_user = jogging.user
    jogging_user_role = jogging_user.role
    
    if role == ROLE.MANAGER.value and (jogging_user.id != current_user.id and jogging_user_role.name in [ROLE.MANAGER.value, ROLE.ADMIN.value]):
        raise HTTPException(status_code=401, detail="Permission denied")
    
    return jogging_service.update(db, obj_in=jogg)


@router.get('/joggings', response_model=ListJoggings, tags=['jogging'])
def get_all_joggings(
    page: int,
    db: Session = Depends(get_db),
    current_user: JoggingCreate = Depends(get_current_user)
):
    role = getattr(getattr(current_user, 'role'), 'name', None)
   
    if role == ROLE.ADMIN.value:
        return jogging_service.get_paginate(db, page=page)  
    
    query = db.query(JoggingModel).join(JoggingModel.user).join(User.role)
    
    filters = []
    filters.append(getattr(JoggingModel, 'user_id') == current_user.id)
    
    if role == ROLE.MANAGER.value:
        filters.append(Role.name == ROLE.BASIC.value)
        
    if len(filters) > 0:
        query = query.filter(or_(*filters))
        
    return jogging_service.get_paginate_raw_query(query, page=page)
