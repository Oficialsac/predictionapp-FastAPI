class ErrorResponse:
    INVALID_USERNAME = {'description': 'Invalid username', 'success': False}
    INVALID_USERNAME_PASSWORD = {'description': 'Invalid password', 'success': False}
    USER_DOESNT_EXIST = {'description': 'User does not exist', 'success': False}
    USER_ALREADY_EXIST = {'description': 'Invalid already exists', 'success': False}
    