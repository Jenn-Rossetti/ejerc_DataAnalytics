from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import logging
import psycopg2
import pandas as pd
import datetime
from decouple import config
import os

"""
DAG Description:
DAG para obtener datos del grupo de universidades E desde la base de datos
"""

#logging config
logging.basicConfig(
    level=logging.INFO,
    datefmt='%Y-%m-%d',
    format='%(asctime)s: %(levelname)s - %(message)s',
)

def query_universities_e():
    #conexión db
    logging.info('Conectando a la DB')
    conn = psycopg2.connect(
                host=config("HOST"),
                user=config("Alkymer"),
                password=config("Alkemy22"),
                database=config("DATABASE")
    )

    #cursor
    cur = conn.cursor()

    #definición de queries
    with open("query_universities_e.sql", encoding='utf-8') as query_file:
        content = query_file.read()
        queries = content.split("-- Universidad Nacional De La Pampa")

    #ejecuta queries
    logging.info('Ejecutando las consultas a la DB')
    cur.execute(queries[0])
    result_moron_pampa = cur.fetchall()

    cur.execute(queries[1])
    result_interamericana = cur.fetchall()

    #resultados de queries a csv
    df_moron_pampa = pd.DataFrame(result_moron_pampa)
    df_interamericana = pd.DataFrame(result_interamericana)

    logging.info('Guardando los resultados')
    
    #crea carpeta para guardar
    outdir = './files'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    #guarda archivos resultantes
    outname = 'universidad_moron_pampa.csv'
    fullname = os.path.join(outdir, outname)
    df_moron_pampa.to_csv(fullname)

    outname = 'universidad_interamericana.csv'
    fullname = os.path.join(outdir, outname)
    df_interamericana.to_csv(fullname)

    logging.info('Consultas finalizadas')

    cur.close()
    conn.close()
    logging.info('Conexión con la DB cerrada')



default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
	'sql_operator',
	description='get universities of group e from sql',
    default_args=default_args,
	schedule_interval='@hourly',
	start_date=datetime(2022, 7, 23),
) as dag:
	get_data = PythonOperator(
        task_id ='get data from sql',
        python_callable = query_universities_e
    )

	get_data