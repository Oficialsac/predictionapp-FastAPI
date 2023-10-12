import joblib
import os
import pandas as pd
from fastapi import UploadFile

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir,'joblib_linear.pkl')

def read_ml_model():
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        return model
    
    
def dataframe_to_html(dataframe: pd.DataFrame):
    return dataframe.head(50).to_json()


def save_data(file: UploadFile) -> str:
    file_location = f"datasets/{file.filename}"
    
    with open(file_location, 'wb+') as file_obj:
        file_obj.write(file.file.read())
        
    return file_location

    