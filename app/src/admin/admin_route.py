from fastapi import APIRouter
 
router = APIRouter()


@router.get('all_users')
def get_all_users():
    return get_all_users()


@router.put('update_user')
def update_user(userData: str):
    pass
    