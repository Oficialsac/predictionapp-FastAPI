from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    """
    Clase modelo para representar la información de un usuario.

    Atributos:
    - `email` (str): Correo electrónico del usuario.
    - `username` (str): Nombre de usuario.
    - `password` (str): Contraseña del usuario.
    - `role` (Optional[str]): Rol del usuario (opcional, con valor predeterminado "user").
    """
    email: str
    username: str
    password: str
    role: Optional[str] = "user"

class LoginItem(BaseModel):
    """
    Clase modelo para representar los datos de inicio de sesión de un usuario.

    Atributos:
    - `username` (str): Nombre de usuario.
    - `password` (str): Contraseña del usuario.
    """
    username: str
    password: str


