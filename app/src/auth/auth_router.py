from fastapi import APIRouter
from .schemas import User, LoginItem
from auth.service import get_all_users, create_user, get_user_by_username

router = APIRouter()

@router.get('/users')
def get_users():
    """
    Obtiene todos los usuarios registrados.

    Returns:
    - List[User]: Una lista de objetos User representando la información de los usuarios.
    """
    return get_all_users()

@router.post('/register')
def user_register(userdata: User):
    """
    Registra un nuevo usuario.

    Parameters:
    - `userdata` (User): Datos del nuevo usuario a registrar.

    Returns:
    - User: Objeto User que representa la información del usuario recién registrado.
    """
    user = create_user(userdata)
    return user

@router.post('/login')
def user_login(userdata: LoginItem):
    """
    Realiza el inicio de sesión de un usuario.

    Parameters:
    - `userdata` (LoginItem): Datos de inicio de sesión del usuario.

    Returns:
    - User: Objeto User que representa la información del usuario que ha iniciado sesión.
    """
    user = get_user_by_username(userdata)
    return user

    


