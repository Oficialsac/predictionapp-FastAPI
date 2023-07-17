import json
from auth.schemas import User
from auth.utils import *
from auth.constants import ErrorResponse
db = read_file()

def create_user(userData: User) -> User | dict:
    newUser = {
        "username": userData.username,
        "password": userData.password
    }
    for user in db:
        if user['username'] == newUser.get('username'):
            return  ErrorResponse.USER_ALREADY_EXIST
    db.append(newUser)
    return {'user':newUser, 'success':True}
    

def get_user_by_username(userData: User) -> User | dict:
    for user in db:
        if user['username'] == userData.username:
            
            if user['password'] == userData.password:
                return user
            else: 
                return ErrorResponse.INVALID_USERNAME_PASSWORD
    return ErrorResponse.USER_DOESNT_EXIST

def get_all_users() -> User:
    return db
