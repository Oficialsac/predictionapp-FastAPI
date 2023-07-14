from pydantic import BaseModel
from typing import Optional, Optional

class User(BaseModel):
    username: str 
    password: str
    admin: Optional[bool] = False
