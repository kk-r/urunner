from models import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time, JSON


class Jogging(Base):
    __tablename__ = 'user_jogging_data'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    distance = Column(Integer, nullable=False)
    time = Column(Time, nullable=False)
    location = Column(String(80), nullable=False)
    weather_condition = Column(JSON, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User')
