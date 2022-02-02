from models import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255))
    role_id = Column(Integer, ForeignKey('roles.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    role = relationship('Role')
