from typing import List
from pydantic import BaseModel
from .response import Pagination


class RoleBase(BaseModel):
    name: str


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True
