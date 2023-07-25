from fastapi import APIRouter
from ml_models.schemas import PredictionVariables
from ml_models.services import get_prediction

router = APIRouter()

@router.post('/prediction')
def create_prediction(variablesValues: PredictionVariables):
    return {"": get_prediction(variablesValues)[0]}