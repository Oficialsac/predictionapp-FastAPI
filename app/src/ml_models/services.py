import pandas as pd
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from ml_models.schemas import PredictionVariables
from ml_models.utils import save_data
from .notebooks.modelProcesing import DataModelProcessing
import json
import os

file_locations = []
path_datasets = os.path.join(os.getcwd(), 'datasets')
obj = DataModelProcessing(path=path_datasets)

def get_prediction(variables: PredictionVariables):
    """
    Realiza una predicción utilizando las variables proporcionadas.

    Parameters:
    - `variables` (PredictionVariables): Variables para la predicción.

    Returns:
    - dict: Resultado de la predicción.
    """
    dict_to_return = {}
    
    if len(obj.datasets) > 0:
        dataset = obj.transform_datasets(programa=variables.programa)
        dataset = obj.transform_to_model(dataset)
        print(dataset)
        if not dataset['error']:
            model = obj.train_model()
            results = obj.predictions(variables.datos, STEPS=obj.calcular_steps(variables.datos, variables))
            results_json = json.loads(results.to_json(orient='table'))['data']
            data_history = json.loads(obj.datasets_to_model[variables.datos].to_json(orient='table'))['data']
        
            dict_to_return = {
                'vars': variables,
                'data': data_history,
                'pred_info': results_json,
                'status': True
            }
        else:
            dict_to_return = {
                'status': False
            }
    
    return dict_to_return

def upload_file(file: UploadFile):
    """
    Carga un archivo de datos y guarda la ubicación del archivo en la lista `file_locations`.

    Parameters:
    - `file` (UploadFile): Archivo de datos a cargar.

    Returns:
    - dict: Devuelve un diccionario indicando el estado de la carga.
    """
    if file.content_type == "text/csv":
        file_locations.append(save_data(file))
        if len(file_locations) == 4:
            if os.listdir(path_datasets):
                obj.load_datasets()
                return JSONResponse(content={"status_load": True, "data": obj.datasets['inscritos'].head(10).to_json()})
    else: 
        return {'status_load': None}
    
    return {'status_load': False}

def training_model_service():
    """
    Inicia el proceso de entrenamiento del modelo.

    Returns:
    - None
    """
    try:
        if len(obj.datasets) > 0:
            dataset = obj.transform_datasets()
            obj.transform_to_model(dataset_to_transform=dataset)
            model = obj.train_model()
            print("training_model: ", type(model), model)
            return model
        else:
            print('NO HAY DATA')
    except Exception as e:
        print(e)



def get_statistics_service():
    datos = obj.descriptive_analysis('graduados')
    return JSONResponse(content=datos)
    