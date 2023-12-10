from fastapi import APIRouter, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from ml_models.schemas import PredictionVariables
from ml_models.services import get_prediction, upload_file, training_model_service
import json

router = APIRouter()

@router.post('/prediction')
def create_prediction(variablesValues: PredictionVariables):
    """
    Realiza una predicción utilizando variables proporcionadas.

    Parameters:
    - `variablesValues` (PredictionVariables): Variables para la predicción.

    Returns:
    - dict: Resultado de la predicción.
    """
    return get_prediction(variablesValues)

@router.post("/training", response_class=JSONResponse) 
def training_data(file: UploadFile):
    """
    Carga datos de entrenamiento desde un archivo y realiza el entrenamiento del modelo.

    Parameters:
    - `file` (UploadFile): Archivo de datos de entrenamiento.

    Returns:
    - JSONResponse: Respuesta JSON que proporciona información sobre el entrenamiento.
    """
    data = upload_file(file)
    return data

@router.post("/training_data")
def training_model():
    """
    Inicia el proceso de entrenamiento del modelo.

    Returns:
    - str: Mensaje indicando que el entrenamiento del modelo ha comenzado.
    """
    model_training = training_model_service()
    return 'JSONResponse(model_training)'
