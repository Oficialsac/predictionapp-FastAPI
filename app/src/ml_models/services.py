import pandas as pd
from fastapi import UploadFile
from ml_models.schemas import PredictionVariables
from ml_models.utils import *
from .notebooks.procesingData import *


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
    
    
def upload_file(file: UploadFile):
    if (file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or file.content_type == "text/csv"):
        file_location = save_data(file)
        if( file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
            df = pd.read_excel(file_location)
            pr = procesingData(df=df)
            dataset = pr.imputeData()
            
            return  dataframe_to_html(dataset)
        elif (file.content_type == "text/csv"):
            df = pd.read_csv(file_location)
            pr = procesingData(df=df)
            dataset = pr.imputeData()
            
            return dataframe_to_html(dataset)
    else: 
        return '<h1> ARCHIVO NO VALIDO <h1/>'
    
    return '<h1> SIN CONTENIDO <h1/>'
        


