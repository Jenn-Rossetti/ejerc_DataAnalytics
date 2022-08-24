from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook


def upload_to_s3(filename: str,  bucket_name: str) -> None:
    hook = S3Hook('s3_conn')
    hook.load_file(filename=filename, key=key, bucket_name=bucket_name)


with DAG(
	's3_univ_E',
	description='s3 para universidad Nacional de La Pampa y Universidad Abierta Interamericana',
	schedule_interval=timedelta(days = 1 ),
    start_date=datetime(2022, 7, 25),
    catchup=False
) as dag:
    
    task_upload_to_s3_interamericana= PythonOperator(
        task_id= 'upload_to_s3_i',
        python_callable= upload_to_s3,
        op_kwargs={
            ##simulo los archivos .txt porque no los tengo 
            'filename': '/home/jennifer/airflow/dags/universidad_e_normalized.txt',
            'key': 'universidad_e_normalized.txt',
            #este dato 'cohorte' fue copiado de slack por lo que puede no ser correcto para mi grupo de universidades
             # se debe reemplazar al obtener el archivo .txt
            'bucket_name': 'cohorte-julio-a192d78b'
            }
    )

    task_upload_to_s3_LaPampa= PythonOperator(
        task_id= 'upload_to_s3_p',
        python_callable= upload_to_s3,
        op_kwargs={
            ##simulo los archivos .txt porque no los tengo 
            'filename': '/home/jennifer/airflow/dags/universidad_e_normalized.txt',
            'key': 'universidad_e_normalized.txt',
            #este dato 'cohorte' fue copiado de slack por lo que puede no ser correcto para mi grupo de universidades
             # se debe reemplazar al obtener el archivo .txt
            'bucket_name': 'cohorte-julio-a192d78b'
            }
    )
    task_upload_to_s3_interamericana >> task_upload_to_s3_LaPampa