class ErrorResponse:
    """
    Clase que define respuestas de error predefinidas.

    Atributos:
    - `USER_DOESNT_EXIST` (dict): Respuesta para el caso en que el usuario no existe.
      - `description` (str): Descripción del error, indicando que el usuario no existe.
      - `success` (bool): Indicador de éxito (False en este caso, ya que es una respuesta de error).
    """
    USER_DOESNT_EXIST = {'description': 'Usuario no existe', 'success': False}
