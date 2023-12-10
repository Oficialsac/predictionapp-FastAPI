import joblib
import os
import pandas as pd
from fastapi import UploadFile

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'joblib_linear.pkl')

def read_ml_model():
    """
    Lee el modelo de aprendizaje automático desde el archivo.

    Returns:
    - object: Objeto del modelo de aprendizaje automático.
    """
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        return model

def dataframe_to_html(dataframe: pd.DataFrame) -> str:
    """
    Convierte un DataFrame de pandas a formato HTML.

    Parameters:
    - `dataframe` (pd.DataFrame): DataFrame de pandas.

    Returns:
    - str: Representación HTML del DataFrame.
    """
    return dataframe.head(50).to_json()

def save_data(file: UploadFile) -> str:
    """
    Guarda el archivo de datos en la carpeta 'datasets'.

    Parameters:
    - `file` (UploadFile): Archivo de datos a guardar.

    Returns:
    - str: Ruta del archivo guardado.
    """
    file_location = f"datasets/{file.filename}"
    
    with open(file_location, 'wb+') as file_obj:
        file_obj.write(file.file.read())
        
    return file_location


    