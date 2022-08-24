import pandas as pd
from airflow import DAG
import numpy as np
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator

def process_data():

    def process_abierta_interamericana():

        df_interamericana = pd.read_csv("files/universidad_interamericana.csv") 

        #elimina primera columna (indices)
        df_interamericana = df_interamericana.iloc[: , 1:]

        #nuevos nombres de columnas
        df_interamericana.columns = ["university", "career", "inscription_date", "name", "gender", "age", "location", "email"] 

        #minusculas y elimina guiones de university
        df_interamericana["university"] = df_interamericana["university"].str.replace("-"," ")
        df_interamericana["university"] = df_interamericana["university"].str.lower()

        #elimina guiones y espacios de career
        df_interamericana["career"] = df_interamericana["career"].str.replace("-"," ")
        df_interamericana["career"] = df_interamericana["career"].str.strip()

        #formatea date
        df_interamericana["inscription_date"] =  pd.to_datetime(df_interamericana["inscription_date"], format='%d/%b/%y')
        df_interamericana["inscription_date"] =  pd.to_datetime(df_interamericana["inscription_date"], format='%Y/%b/%d')
        df_interamericana['inscription_date'] = df_interamericana['inscription_date'].dt.strftime('%Y-%b-%d')

        #separa columna de nombres
        names = df_interamericana["nombre"].str.split("-", n=1, expand=True)

        #agrega first y last name al df
        df_interamericana["first_name"] = names[0]
        df_interamericana["last_name"] = names[1]
        df_interamericana.drop('name', inplace=True, axis=1)

        #edita columna gender
        df_interamericana.loc[(df_interamericana["gender"] == "M"), "gender"] = "male"
        df_interamericana.loc[(df_interamericana["gender"] == "F"), "gender"] = "female"

        #minúscula y saca guiones de columna location
        df_interamericana["location"] = df_interamericana["location"].str.lower()
        df_interamericana["location"] = df_interamericana["location"].str.replace("-"," ")

        #lee y prepara codigos postales para merge
        cod_postales = pd.read_csv("codigos_postales.csv", encoding="utf-8")
        cod_postales.rename(columns = {'localidad':'location', 'codigo_postal':'postal_code'}, inplace = True)
        cod_postales["location"] = cod_postales["location"].str.lower()

        #merge
        df_interamericana = df_interamericana.merge(cod_postales, on="location")

        #minúscula de mail column
        df_interamericana["email"] = df_interamericana["email"].str.lower()

        #columna de edad

        #to datetime
        df_interamericana["age"] =  pd.to_datetime(df_interamericana["age"], format='%y/%b/%d')

        #age = fecha de hoy - cumpleaños
        df_interamericana["age"] = pd.Timestamp.now().normalize() - df_interamericana["age"]

        df_interamericana["age"] = df_interamericana["age"].dt.days

        #edad en días dividido el promedio de días en un año
        df_interamericana["age"] = df_interamericana["age"] / 365.2425

        #float to int
        df_interamericana["age"] = df_interamericana["age"].astype(int)

    def process_moron_pampa():

        df_pampa = pd.read_csv("files/universidad_LaPampa.csv")

        #elimina primera columna (indices)
        df_pampa = df_pampa.iloc[: , 1:]

        #nuevos nombres de columnas
        df_pampa.columns = ["university", "career", "inscription_date", "name", "gender", "age", "postal_code", "email"]

        #minusculas y elimina guiones de university
        df_pampa["university"] = df_pampa["university"].str.lower()
        df_pampa["university"] = df_pampa["university"].str.strip()

        #elimina guiones y espacios de career
        df_pampa["career"] = df_pampa["career"].str.lower()
        df_pampa["career"] = df_pampa["career"].str.strip()

        #formatea date
        df_pampa["inscription_date"] =  pd.to_datetime(df_pampa["inscription_date"], format='%d/%m/%Y')
        df_pampa["inscription_date"] =  pd.to_datetime(df_pampa["inscription_date"], format='%Y/%b/%d')
        df_pampa['inscription_date'] = df_pampa['inscription_date'].dt.strftime('%Y-%b-%d')

        #separa columna de nombres
        names = df_pampa["name"].str.split(" ", n=1, expand=True)

        #agrega first y last name al df
        df_pampa["first_name"] = names[0]
        df_pampa["last_name"] = names[1]
        df_pampa.drop('name', inplace=True, axis=1)

        #edita columna gender
        df_pampa.loc[(df_pampa["gender"] == "M"), "gender"] = "male"
        df_pampa.loc[(df_pampa["gender"] == "F"), "gender"] = "female"

        #lee y prepara codigos postales para merge
        df_pampa["postal_code"] = df_pampa["postal_code"].astype(int)
        cod_postales = pd.read_csv("codigos_postales.csv", encoding="utf-8")
        cod_postales.rename(columns = {'localidad':'location', 'codigo_postal':'postal_code'}, inplace = True)
        cod_postales["location"] = cod_postales["location"].str.lower()

        #merge
        df_pampa = df_pampa.merge(cod_postales, on="postal_code")

        #minúscula de mail column
        df_pampa["email"] = df_pampa["email"].str.lower()

        #format columa de edad

        #to datetime
        df_pampa["age"] =  pd.to_datetime(df_pampa["age"], format='%d/%m/%Y')

        df_pampa["age"] = pd.Timestamp.now().normalize() - df_pampa["age"]

        #datetime days to int
        df_pampa["age"] = df_pampa["age"].dt.days

        #edad en días dividido el promedio de días en un año
        df_pampa["age"] = df_pampa["age"] / 365.2425

        #float to int
        df_pampa["age"] = df_pampa["age"].astype(int)

    process_moron_pampa()
    process_abierta_interamericana()

transform_data = PythonOperator(
    task_id="transform",
    python_callable=process_data
)