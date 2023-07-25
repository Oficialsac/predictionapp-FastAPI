from pydantic import BaseModel

class PredictionVariables(BaseModel):
    wheelbase: float
    carlength: float
    carwidth: float
    curbweight: int
    enginesize: int
    boreratio: float
    horsepower: int
    citympg: int
    highwaympg: int