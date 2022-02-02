from sqlalchemy.orm import Session
from typing import Union, Dict, Any
from fastapi.encoders import jsonable_encoder

from models import Jogging
from db.crud import CRUDBase
from core.helper import get_weather_condition_data
from models.user import User
from schemas.jogging import JoggingCreate, JoggingUpdate


class CRUDJogging(CRUDBase[Jogging, JoggingCreate, JoggingUpdate]):
    def create(self, db: Session, *, obj_in: JoggingCreate, current_user: User) -> Jogging:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['weather_condition'] = get_weather_condition_data(obj_in_data['location'])
        obj_in_data['user_id'] = current_user.id
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session,
        *, obj_in: Union[JoggingUpdate, Dict[str, Any]]
    ) -> Jogging:
        db_obj = db.query(self.model).get(obj_in.id)
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            print(field in update_data, field == 'location', update_data['location'])
            if field in update_data and field != 'weather_condition':
                setattr(db_obj, field, update_data[field])
            if field in update_data and field == 'location':
                db_obj.weather_condition = get_weather_condition_data(update_data['location'])
                
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


jogging_service = CRUDJogging(model=Jogging)
