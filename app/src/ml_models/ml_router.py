from fastapi import APIRouter, UploadFile
from fastapi.responses import HTMLResponse
from ml_models.schemas import PredictionVariables
from ml_models.services import get_prediction, upload_file

router = APIRouter()

@router.post('/prediction')
def create_prediction(variablesValues: PredictionVariables):
    return {"values": get_prediction(variablesValues)[0]}

@router.post("/training", response_class=HTMLResponse)
def training_data(file: UploadFile):
    return upload_file(file)