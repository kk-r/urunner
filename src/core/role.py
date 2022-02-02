import os
from enum import Enum


class ROLE(Enum):
    ADMIN: str = os.getenv('ADMIN', 'ADMINISTRATOR')
    BASIC: str = os.getenv('BASIC', 'BASIC')
    MANAGER: str = os.getenv('MANAGER', 'MANAGER')
