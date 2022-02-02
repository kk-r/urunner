from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenUser(Token):
    role_id: Optional[int]
    role_name: Optional[str]


class TokenData(BaseModel):
    username: Optional[str] = None
