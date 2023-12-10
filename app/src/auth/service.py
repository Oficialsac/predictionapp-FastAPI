import json
from .schemas import User, LoginItem
from auth.utils import read_file
from auth.constants import ErrorResponse

# Leer datos desde el archivo
db = read_file()

def create_user(userData: User) -> User | dict:
    """
    Crea un nuevo usuario y lo agrega a la base de datos.

    Parameters:
    - `userData` (User): Datos del nuevo usuario a registrar.

    Returns:
    - Union[User, dict]: Devuelve el objeto User recién creado si el registro es exitoso.
      En caso de error, devuelve un diccionario con un mensaje de error.
    """
    new_user = {
        "email": userData.email,
        "username": userData.username,
        "password": userData.password,
        "rol": 'user'
    }

    # Verificar si el usuario ya existe
    for user in db:
        if user['username'] == new_user.get('username'):
            return ErrorResponse.USER_ALREADY_EXIST

    # Agregar el nuevo usuario a la base de datos
    db.append(new_user)
    
    return {'user': new_user, 'success': True}

def get_user_by_username(userData: LoginItem) -> dict:
    """
    Obtiene un usuario por nombre de usuario y verifica las credenciales.

    Parameters:
    - `userData` (LoginItem): Datos de inicio de sesión del usuario.

    Returns:
    - dict: Devuelve un diccionario con información del usuario si las credenciales son válidas.
      En caso de error, devuelve un diccionario con un mensaje de error.
    """
    for user in db:
        if user['username'] == userData.username:
            if user['password'] == userData.password:
                return {'user': user, 'success': True}
            else:
                return ErrorResponse.INVALID_USERNAME_PASSWORD
    return ErrorResponse.USER_DOESNT_EXIST

def get_all_users() -> User:
    """
    Obtiene todos los usuarios registrados.

    Returns:
    - User: Devuelve la lista de usuarios registrados.
    """
    return db
