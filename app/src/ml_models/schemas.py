from pydantic import BaseModel

class PredictionVariables(BaseModel):
    """
    Clase modelo para representar las variables necesarias para realizar una predicción.

    Atributos:
    - `datos` (str): Datos para la predicción.
    - `anio` (str): Año para la predicción.
    - `semestre` (str): Semestre para la predicción.
    - `programa` (str): Programa para la predicción.
    """
    datos: str
    anio: str
    semestre: str
    programa: str
