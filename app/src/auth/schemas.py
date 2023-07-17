from pydantic import BaseModel
from typing import Optional, Optional

class User(BaseModel):
    username: str 
    password: str
    role: Optional[str] = "user"
