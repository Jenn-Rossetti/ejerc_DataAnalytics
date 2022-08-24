from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import time
from sqlalchemy import  exc, create_engine, inspect
from decouple import config

def check_db_connectioncheck_db_connection():
    retry_flag = True
    retry_count = 0 
    while retry_flag and retry_count < 10:
        try:
            engine = create_engine(config('DB_DATA_CONNECT'))
            engine.connect()
            insp = inspect(engine)
            #se comprueba si existen las tablas, de no ser asi se reeintenta la conexion
            if insp.has_table("moron_nacional_pampa") and insp.has_table("rio_cuarto_interamericana"):
                retry_flag = False
            else: 
                retry_count = retry_count + 1 
                time.sleep(60)
        except exc.SQLAlchemyError:
            #se incrementa la variable de control en caso de que se produzca un error
            retry_count = retry_count + 1
            #s espera 1 minuto antes de el siguiente reintento
            time.sleep(60)


default_args = {
    'retries':5,
    'retry_delay': timedelta(seconds=30)
}

#se definen las propiedades del dag.
with DAG(
    'check_db_connection',
    description='comprobar la conexion con la db.',
    schedule_interval=timedelta(days = 1 ),
    start_date=datetime(2022, 7, 15),
    ) as dag:
    
    task_check_db_connection = PythonOperator(
        task_id = 'check_db_connection',
        python_callable = 'check_db_connection'
        )