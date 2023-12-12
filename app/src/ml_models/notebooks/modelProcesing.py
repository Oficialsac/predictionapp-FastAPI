import warnings
import os
from functools import lru_cache
import json

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import statsmodels.api as sm
import seaborn as sns

from skforecast.Sarimax import Sarimax
from pmdarima import auto_arima

warnings.filterwarnings("ignore")

class DataModelProcessing:

    def __init__(self, path):
        """
        Inicializa la instancia de la clase DataModelProcessing.

        Parameters:
        - `path` (str): Ruta donde se encuentran los conjuntos de datos.
        """
        self.path = path
        self.datasets = {}
        self.datasets_to_model = {}
        self.dataset = pd.DataFrame()
        self.model = {}
    
    def load_datasets(self):
        """
        Carga los conjuntos de datos desde la carpeta especificada en la ruta `self.path`.
        """
        file_names = [file for file in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, file))]

        for file_name in file_names:
            file_path = os.path.join(self.path, file_name)
            self.dataset = pd.read_csv(file_path, encoding='ISO-8859-1')
            file_name = file_name.split('_')[1]
            self.datasets[file_name] = self.dataset
            
                
    def filter_dep(self, df, programa: str = None):
        """
        Filtra el conjunto de datos por departamento y, opcionalmente, por programa académico.

        Parameters:
        - `df` (pd.DataFrame): Conjunto de datos original.
        - `programa` (str, optional): Programa académico para filtrar el conjunto de datos.

        Returns:
        - pd.DataFrame: Conjunto de datos filtrado.
        """
        df = df[df['code_dep'] == 5]
        if programa is not None:
            df = df[df['prog_aca'] == programa]
            if df.shape[0] < 10:
                return None
            return df
        return df

    def pipeline_data_processing(self, data_without_processing_copy, programa: str = None):
        """
        Aplica un procesamiento de datos al conjunto de datos.

        Parameters:
        - `data_without_processing_copy` (pd.DataFrame): Conjunto de datos sin procesar.
        - `programa` (str, optional): Programa académico para filtrar el conjunto de datos.

        Returns:
        - pd.DataFrame: Conjunto de datos procesado.
        """
        try:
            df = self.filter_dep(data_without_processing_copy, programa)
            return df
        except Exception as e:
            print(e)
        
    def transform_datasets(self, programa: str = None):
        """
        Transforma los conjuntos de datos cargados aplicando el procesamiento necesario.

        Parameters:
        - `programa` (str, optional): Programa académico para filtrar el conjunto de datos.

        Returns:
        - dict: Diccionario de conjuntos de datos transformados.
        """
        temp_dataset = {}
        
        for dataset_name in self.datasets.keys():
            temp_dataset[dataset_name] = self.pipeline_data_processing(self.datasets[dataset_name], programa)
            
        return temp_dataset
            
    def transform_to_model(self, dataset_to_transform):
        """
        Transforma el conjunto de datos para su uso en el modelo.

        Parameters:
        - `dataset_to_transform` (dict): Diccionario de conjuntos de datos transformados.

        Returns:
        - dict: Diccionario de conjuntos de datos listos para el modelo.
        """
        best_parameters = {}
        for dataset_name in self.datasets.keys():
            if dataset_to_transform[dataset_name] is not None:
                dataset_modified = {}   
                dataset_modified[dataset_name] = (dataset_to_transform[dataset_name][['year','sem','conteo']]
                .reset_index(drop=True)
                .assign(
                    sem = lambda df: df['sem'].map({1:'01', 2:'07'})
                )
                .assign(
                    date=lambda df: pd.to_datetime(df['year'].astype(str)+'-'+df['sem'].astype(str)+'-'+'01')
                )
                .set_index('date')
                .drop(columns=['year','sem']) 
                )
                
                dataset_modified[dataset_name] = dataset_modified[dataset_name].groupby(dataset_modified[dataset_name].index).agg({'conteo':'sum'})
                if dataset_modified[dataset_name].shape[1] == 1:
                    best_parameters.update(dataset_modified) 
            else:
                return {'error': True, 'description': 'No dataset found'}   
            
        print(best_parameters)
        self.datasets_to_model = best_parameters
        return {'error': False, 'description': 'None'}  
            
            
    def train_model(self):
        """
        Entrena el modelo utilizando el conjunto de datos transformado.

        Returns:
        - dict: Diccionario de modelos entrenados.
        """
        for dataset in self.datasets.keys():
            # Seleccionar los mejores parámetros
            best_parameters = auto_arima(self.datasets_to_model[dataset]['conteo'], start_p=0, d=None, start_q=0, max_p=3, max_q=3,
                            seasonal=True, m=1, D=None, test='adf', start_P=0, start_Q=0, max_P=3, max_Q=3,
                            information_criterion='aic', trace=True, error_action='ignore',
                            trend=None, with_intercept=True, stepwise=True)
        
            # Parámetros ARIMA --------------------------------------------------------------
            p, d, q = (best_parameters.get_params()['order'][0],
                       best_parameters.get_params()['order'][1],
                       best_parameters.get_params()['order'][2])
            
            # Parámetros estacionales --------------------------------------------------------
            P, D, Q, m = (best_parameters.get_params()['seasonal_order'][0],
                          best_parameters.get_params()['seasonal_order'][1],
                          best_parameters.get_params()['seasonal_order'][2],
                          best_parameters.get_params()['seasonal_order'][3])
            
            # Instanciar modelo y ajustar
            skmodel = Sarimax(order=(p, d, q), seasonal_order=(P, D, Q, 6))
            stmodel = sm.tsa.statespace.SARIMAX(self.datasets_to_model[dataset]['conteo'], order=(p, d, q), seasonal_order=(P, D, Q, m)) 
            
            skmodel.fit(self.datasets_to_model[dataset]['conteo'].values)
            stmodel_fit = stmodel.fit()
            
            st_model_aic, sk_model_aic = stmodel_fit.aic, skmodel.get_info_criteria(criteria='aic')
            
            if st_model_aic < sk_model_aic:
                self.model.update({dataset: stmodel_fit})
            else: 
                self.model.update({dataset: skmodel})
                
        return self.model
    
    def calcular_steps(self, DATA_NAME: str, variables):
        """
        Calcula el número de pasos para predecir en base a las variables proporcionadas.

        Parameters:
        - `DATA_NAME` (str): Nombre del conjunto de datos.
        - `variables` (PredictionVariables): Variables de predicción.

        Returns:
        - int: Número de pasos a predecir.
        """
        año_prediccion = pd.to_datetime(f"{variables.anio}-{'07' if variables.semestre == '2' else '01'}-01")
        ultimo_año = self.datasets_to_model[DATA_NAME].index.max()
        
        steps = 0
        time_diference = año_prediccion - ultimo_año
        rest = int(time_diference.days)
        while rest > 0:
            rest = rest - 182
            steps = steps + 1
            
        return steps - 1
                
    def generar_intervalo(self, initial_dates, steps):
        """
        Genera un intervalo de fechas para las predicciones.

        Parameters:
        - `initial_dates` (list): Lista de fechas iniciales.
        - `steps` (int): Número de pasos.

        Returns:
        - list: Lista de fechas generadas.
        """
        initial_dates = pd.to_datetime(initial_dates)
        
        freq = (initial_dates[2] - initial_dates[1])
        
        last_date = initial_dates.max()
        new_dates = pd.date_range(start=last_date, periods=steps + 1, freq=freq)[1:]
        
        new_dates_str = new_dates.strftime('%Y-%m-%d').tolist()
        
        for i, dates in enumerate(new_dates_str):
            split_dates = dates.split('-')
            if split_dates[2] != '01':
                date = f"{split_dates[0]}-{split_dates[1]}-01"
                new_dates_str[i] = date
            else:
                new_dates_str[i] = dates
            
        return new_dates_str

    def predictions(self, DATA_NAME: str, STEPS: int = 1):
        """
        Realiza predicciones utilizando el modelo entrenado.

        Parameters:
        - `DATA_NAME` (str): Nombre del conjunto de datos.
        - `STEPS` (int, optional): Número de pasos a predecir.

        Returns:
        - pd.DataFrame: DataFrame con las predicciones.
        """
        data_options = {'inscritos', 'matriculados', 'admitidos', 'graduados'}
        
        if DATA_NAME not in data_options:
            raise ValueError("Data parameter does not exist, expected 'inscritos', 'matriculados', 'admitidos', 'graduados'")
        
        if type(STEPS) == str:
            raise TypeError(f"Error: Expected 'steps' to be of type int, but received {type(STEPS).__name__}.")
        
        results = self.model[DATA_NAME].predict(steps=STEPS, return_conf_int=True)
            
        # Crear conjunto de datos con predicciones
        dataset_index = self.datasets_to_model[DATA_NAME].index
        time_interval = self.generar_intervalo(dataset_index, STEPS)

        return pd.DataFrame(results).set_index(pd.to_datetime(time_interval))
    
    def descriptive_analysis(self, DATA_NAME: str):
        data_options = {'inscritos', 'matriculados', 'admitidos', 'graduados'}
            
        if DATA_NAME not in data_options:
            raise ValueError("Data parameter does not exist, expected 'inscritos', 'matriculados', 'admitidos', 'graduados'")
            
        dict_to_return = {}

        ch1 = self.datasets[DATA_NAME].groupby(['nom_ies']).agg({'conteo':'sum'}).head(20)
        dict_ch1 = {
            'index': ch1.index.tolist(),
            'values': ch1['conteo'].tolist()
        }   

        ch2 = self.datasets[DATA_NAME].groupby(['prog_aca']).agg({'conteo':'sum'}).head(20)
        dict_ch2 = {
            'index': ch2.index.tolist(),
            'values': ch2['conteo'].tolist()
        } 
        
        
        
        ch3 = self.datasets[DATA_NAME].groupby(['sem']).agg({'conteo':'sum'}).head(20)
        dict_ch3 = {
            'index': ch3.index.tolist(),
            'values': ch3['conteo'].tolist()
        } 
        
        
        ch4 = self.datasets[DATA_NAME].groupby(['nom_dep']).agg({'conteo':'sum'}).head(20)
        dict_ch4 = {
            'index': ch4.index.tolist(),
            'values': ch4['conteo'].tolist()
        } 
                
        dict_to_return = {
            'chart1': dict_ch1,
            'chart2': dict_ch2,
            'chart3': dict_ch3,
            'chart4': dict_ch4,
        }
            
        return dict_to_return
            
    
