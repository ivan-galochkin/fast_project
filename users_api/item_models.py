from typing import Optional
from pydantic import BaseModel


class UserItem(BaseModel):
    email: Optional[str]
    password: Optional[str]
