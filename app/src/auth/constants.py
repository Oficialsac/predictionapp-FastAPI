class ErrorResponse:
    """
    Clase que define respuestas de error predefinidas.

    Atributos:
    - `INVALID_USERNAME` (dict): Respuesta para el caso de nombre de usuario inválido.
      - `description` (str): Descripción del error, indicando que el nombre de usuario es inválido.
      - `success` (bool): Indicador de éxito (False en este caso, ya que es una respuesta de error).

    - `INVALID_USERNAME_PASSWORD` (dict): Respuesta para el caso de contraseña inválida.
      - `description` (str): Descripción del error, indicando que la contraseña es inválida.
      - `success` (bool): Indicador de éxito (False en este caso, ya que es una respuesta de error).

    - `USER_DOESNT_EXIST` (dict): Respuesta para el caso en que el usuario no existe.
      - `description` (str): Descripción del error, indicando que el usuario no existe.
      - `success` (bool): Indicador de éxito (False en este caso, ya que es una respuesta de error).

    - `USER_ALREADY_EXIST` (dict): Respuesta para el caso en que el usuario ya existe.
      - `description` (str): Descripción del error, indicando que el usuario ya existe.
      - `success` (bool): Indicador de éxito (False en este caso, ya que es una respuesta de error).
    """
    INVALID_USERNAME = {'description': 'Nombre de usuario inválido', 'success': False}
    INVALID_USERNAME_PASSWORD = {'description': 'Contraseña inválida', 'success': False}
    USER_DOESNT_EXIST = {'description': 'El usuario no existe', 'success': False}
    USER_ALREADY_EXIST = {'description': 'El usuario ya existe', 'success': False}
