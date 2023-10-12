from fastapi import APIRouter, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from ml_models.schemas import PredictionVariables
from ml_models.services import get_prediction, upload_file

router = APIRouter()

@router.post('/prediction')
def create_prediction(variablesValues: PredictionVariables):
    return get_prediction(variablesValues)

@router.post("/training", response_class=JSONResponse) 
def training_data(file: UploadFile):
    return upload_file(file)