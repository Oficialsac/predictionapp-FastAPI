from pydantic import BaseModel
from typing import Optional, Optional

class User(BaseModel):
    email: str
    username: str 
    password: str
    role: Optional[str] = "user"
    
    
class LoginItem(BaseModel):
    username: str 
    password: str

