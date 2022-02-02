import json
from typing import List, Optional
from datetime import date as date_type
from datetime import time as time_type

from pydantic import BaseModel
from .response import Pagination


class JoggingInDbBase(BaseModel):
    date: date_type 
    distance: int
    time: time_type
    location: str
        
    class Config:
        orm_mode = True

class Jogging(JoggingInDbBase):
    id: int
    user_id: int
       
class JoggingCreate(JoggingInDbBase):
    weather_condition: Optional[dict]

class JoggingUpdate(JoggingInDbBase):
    id: int
    weather_condition: Optional[dict]

class JoggingComplete(JoggingInDbBase):
    weather_condition: Optional[dict]
    user_id: int
    
class ListJoggings(Pagination):
    data: List[JoggingComplete]

    class Config:
        orm_mode = True
