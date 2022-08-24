from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python_operator import PythonOperator
from scripts.process_data import process_data_univ
from scripts.extract_data import extract_from_db
from scripts.upload_file import upload_to_s3
import logging

#configuración del login
logging.basicConfig(level=logging.INFO,
                    datefmt='%Y-%M-%D',
                    format='%(nombre)s - %(logger)s - %(mensaje)s'
                    )
logger = logging.getLogger('Universidades-E')
default_args = {
    'owner': 'Airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dag_OT254-32',
    description='configurar DAG para el grupo de universidades E',
    default_args=default_args,
    schedule_interval=timedelta(hours=1),
    start_date=datetime(2022, 7, 17),
) as dag:

    logger.info("")
    #tareas ficticias que se pueden cambiar según la necesidad
    extract = PythonOperator(task_id='extract',
                             python_callable=extract_from_db,
                             retries=5,
                             retry_delay=timedelta(minutes=5))
    transform = PythonOperator(task_id='transform',
                               python_callable=process_data_univ)
    load = PythonOperator(task_id='load',
                          python_callable=upload_to_s3)

    extract >> transform >> load