from fastapi import APIRouter
from auth.schemas import User
from auth.service import *
router = APIRouter()

@router.get('/users')
def get_users():
    return get_all_users()

@router.post('/register')
def user_register(userdata: User):
    user = create_user(userdata)
    return user


@router.post('/login')
def user_login(userdata: User):
    user = get_user_by_username(userdata)
    return user
    
    


