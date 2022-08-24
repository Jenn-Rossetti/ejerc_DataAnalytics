from airflow import DAG
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from decouple import config
import logging
import pandas as pd
from airflow.operators.python_operator import PythonOperator

def procesar_datos():
        #se leen los archivos sql de las universidades
        file = open('univ_LaPampa.sql','r' )
        univ_moron_pampa_sql = file.read()
        file = open('univ_Interamericana.sql','r' )
        univ_interamericana_sql = file.read()

        #Se ejecutan laa consultas sql correspondientes a cada universidad y se genera un dataframe para cada una.
        df_unv_pampa = pd.read_sql(univ_moron_pampa_sql, config('DB_DATA_CONNECT'))
        df_unv_interamericana = pd.read_sql(univ_interamericana_sql, config('DB_DATA_CONNECT'))

        #se guardan los datos en archivos csv detrno de la carpeta files
        df_unv_pampa.to_csv (r'.\files\unv_pampa.csv', index = None, header=True) 
        df_unv_interamericana.to_csv (r'.\files\unv_interamericana.csv', index = None, header=True) 

#definimos el dag
with DAG(
    'operators_sql',
    description='se procesarn los datos de cada universidad.',
    schedule_interval=timedelta(days = 1 ),
    start_date=datetime(2022, 7, 15),
    ) as dag:
    
    task_data_process = PythonOperator(
        task_id = 'operators_sql',
        python_callable = procesar_datos
    )