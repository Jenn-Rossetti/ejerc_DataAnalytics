import pandas as pd
from airflow import DAG
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from airflow.operators.python_operator import PythonOperator
from procesar_datos import univ_LaPampa_data_process, univ_Interamericana_data_process


#se definen las propiedades del dag.
with DAG(
    'procesar_datos_dag',
    description='dag para procesar los datos de cada universidad',
    schedule_interval=timedelta(days = 1 ),
    start_date=datetime(2022, 7, 23),
    ) as dag:
    
    data_process_univ_LaPampa = PythonOperator(
        task_id = 'procesar datos universidad de la Pampa',
        python_callable = univ_LaPampa_data_process
        )

    data_process_univ_Interamericana = PythonOperator(
        task_id = 'procesar datos univ. abierta ineramericana',
        python_callable = univ_Interamericana_data_process
        )