import pandas as pd
import numpy as np

class procesingData:

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.initialPreProcessing()
        
    def initialPreProcessing(self):
        if(type(self.df["VIGENCIA_AÑOS"].iloc[0]) == str):
            self.df['VIGENCIA_AÑOS'] = self.df['VIGENCIA_AÑOS'].str.replace(',','.').astype(float)
            self.df.drop(columns=['JUSTIFICACION','JUSTIFICACION_DETALLADA','REGISTRO_UNICO'], inplace=True)
            self.df.dropna(subset=['FECHA_EJECUTORIA','RESOLUCIÓN_DE_APROBACIÓN'], inplace=True)
            self.df['VIGENCIA_AÑOS'].fillna(0, inplace=True)
            self.df['RECONOCIMIENTO_DEL_MINISTERIO'].fillna('Sin registro', inplace=True)
            self.df.dropna(inplace=True)
        
    def imputeData(self) -> pd.DataFrame:
        meanCost = self.means_cost()
        meanCost['COSTO_MATRÍCULA_ESTUD_NUEVOS'] = meanCost['COSTO_MATRÍCULA_ESTUD_NUEVOS'].apply(lambda x: int(x))
        
        for id in meanCost['CÓDIGO_INSTITUCIÓN']:
            cost = meanCost[meanCost['CÓDIGO_INSTITUCIÓN'] == id]['COSTO_MATRÍCULA_ESTUD_NUEVOS'].iloc[0]
            creditos = meanCost[meanCost['CÓDIGO_INSTITUCIÓN'] == id]['NÚMERO_CRÉDITOS'].iloc[0]
            self.df.loc[self.df[self.df['CÓDIGO_INSTITUCIÓN'] == id].index,'NÚMERO_CRÉDITOS'] = self.df[self.df['CÓDIGO_INSTITUCIÓN'] == id]['NÚMERO_CRÉDITOS'].fillna(creditos)
            self.df.loc[self.df[self.df['CÓDIGO_INSTITUCIÓN'] == id].index,'COSTO_MATRÍCULA_ESTUD_NUEVOS'] = self.df[self.df['CÓDIGO_INSTITUCIÓN'] == id]['COSTO_MATRÍCULA_ESTUD_NUEVOS'].fillna(cost)
            
        # NEW COLUMN "AÑO" TO KNOWLEDGE WHAT IS THE TIME DURATION OF PROGRAM
        self.df['AÑOS'] = (self.df['FECHA_EJECUTORIA'] - self.df['FECHA_DE_REGISTRO_EN_SNIES']).div(pd.Timedelta(days=365)).astype(int)
        self.df['AÑOS'] = self.df.apply(lambda x: x['AÑOS']+x['VIGENCIA_AÑOS'] if x['ESTADO_PROGRAMA'] == 'Activo' else x['AÑOS'], axis=1)
        
        return self.df
    
    def means_cost(self) -> pd.DataFrame:
        return (
            self.df.groupby(['CÓDIGO_INSTITUCIÓN'])
            .agg({'COSTO_MATRÍCULA_ESTUD_NUEVOS':'mean','NÚMERO_CRÉDITOS':'mean'})
            .reset_index()
        ).fillna(0)
        
    def columns_to_chart(self) -> list:
        return self.df.columns.to_list()
    
    def chart(self, variable_to_chart: str):
        data_to_chart = self.df[variable_to_chart].sum()
        return data_to_chart
    