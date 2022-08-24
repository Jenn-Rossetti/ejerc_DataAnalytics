from airflow import DAG
from datetime import timedelta
import dagfactory

config_file = '/home/jennifer/airflow/dags/dags_config_uni_E.yml'
dag_factory = dagfactory.DagFactory(config_file)
dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())