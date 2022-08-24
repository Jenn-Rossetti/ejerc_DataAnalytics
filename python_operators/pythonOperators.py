import pandas as pd
from airflow import DAG
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from decouple import config


#funcion para procesar datos 
def univ_la_pampa_datos():
    #se lee el archvio sql correspondiente a la universidad de la pampa
    file = open('univ_LaPampa.sql', 'r')
    univ_LaPampa_sql = file.read()
   
    #Se ejecutan las consultas sql y se genera un dataframe .
    df_unv_moron_pampa = pd.read_sql(univ_LaPampa_sql, config('DB_DATA_CONNECT'))

    #se convierte el texo a minusculas de todas las columnas.
    df_unv_moron_pampa = df_unv_moron_pampa.astype(str).apply(lambda x: x.str.lower())

    #se renombran las columnas necesarias
    df_unv_moron_pampa.rename(columns={          
        'universidad':'universidad',          
        'carrerra' : 'carrera',  
        'fechaiscripccion' : 'fecha_inscripcion',                             
        'codgoposstal' : 'codigo_postal',        
        'direccion' : 'direccion',            
        'eemail' : 'email'
        },inplace=True)

   
    #se crea un dataframe con el archivo auxiliar de codigos postales
    df_codigos_postales = pd.read_csv('codigos_postales.csv')       
    #se une el df con los codigos postales con el dataframe de la universidad de la pampa
    df_unv_moron_pampa = pd.merge(df_unv_moron_pampa,df_codigos_postales, how = 'left')
    #se remuve la columna localidad del df de la universidad de la pampa ya que no es requerida
    df_unv_moron_pampa = df_unv_moron_pampa.drop(['localidad'], axis=1)

    #se remplazan los _ por espacios.
    df_unv_moron_pampa["universidad"]= df_unv_moron_pampa["universidad"].str.replace('_', ' ')
    df_unv_moron_pampa["carrerra"]= df_unv_moron_pampa["carrera"].str.replace('_', ' ')
    df_unv_moron_pampa["localidad"]= df_unv_moron_pampa["location"].str.replace('_', ' ')

    #se exportan los datos en un archivo txt
    df_unv_moron_pampa.to_csv('unv_moron_pampa.txt')

#funcion para procesar datos univ. interamericana.
def univ_interamericana():
    #se lee el archvio sql correspondiente a la universidad abierta interamericana
    file = open('univ_Interamericana.sql', 'r')
    univ_interamericana_sql = file.read()

    #Se ejecutan laa consulta sql y se genera un dataframe .
    df_unv_interamericana = pd.read_sql(univ_interamericana_sql, config('DB_DATA_CONNECT'))

    #se renombran las columnas necesarias
    df_unv_interamericana.rename(columns={          
        'univiersities':'universidad',          
        'carrera' : 'carrera',              
        'inscription_dates' : 'fecha_inscripcion',                  
        'codigo_postal' : 'postal_code',        
        'direcciones' : 'direccion',            
        'correo_electronico' : 'email'
        },inplace=True)

    #se convierte el texo a minusculas de todas las columnas.
    df_unv_interamericana = df_unv_interamericana.astype(str).apply(lambda x: x.str.lower())
    #se exportan los datos en un archivo txt
    df_unv_interamericana.to_csv('unv_Interamericana.txt')  