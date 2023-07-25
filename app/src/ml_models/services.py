import pandas as pd
from ml_models.schemas import PredictionVariables
from ml_models.utils import read_ml_model


def get_prediction(variables: PredictionVariables):
        model_to_predict = read_ml_model()
        variables_dictionary = dict(variables)
        X = pd.DataFrame([
            list(
                map(
                    lambda x: variables_dictionary[x], variables_dictionary
                )
            )
        ], columns=variables_dictionary.keys())
        
        results_to_predictions = model_to_predict.predict(X)
        return results_to_predictions
    