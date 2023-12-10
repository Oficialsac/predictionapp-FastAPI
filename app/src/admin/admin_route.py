from fastapi import APIRouter

# Crear una instancia del APIRouter
router = APIRouter()

@router.get('/all_users')
def get_all_users():
    """
    Recupera todos los usuarios.

    Returns:
    - `List[str]`: Una lista con todos los datos de los usuarios.
    """
    return get_all_users()

@router.put('/update_user')
def update_user(userData: str):
    """
    Actualiza los datos de un usuario.

    Parameters:
    - `userData` (str): Los datos actualizados del usuario.

    Returns:
    - None
    """
    pass
