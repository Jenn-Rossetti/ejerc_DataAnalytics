## Tiempo de respuesta promedio en top 0-100 post con mayor puntaje

from respuesta_prom import obt_score, obt_parent_date, mapper_2, mapper_3, reducer, mapper_4, tiempo_respuesta_promedio
from test_top_10 import chunk_data, obtener_datos, mapper
from functools import reduce
from typing import Counter
import xml.etree.ElementTree as ET
import logging
import logging.config
import time
import os


#se especifica la ruta y se crea el registrador
ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#ruta_include = path.abspath(path.join(ruta_base, 'include'))
try:
    logging.config.fileConfig(f'{ruta_base}/data_group_E/logging.cfg')
    
    # create logger
    logger = logging.getLogger('top_10')

except KeyError as e:
   print('No se encontro el archivo logging.cfg en el path especificado.')
   raise e


#se define el dataset sobre el cual se va a realizar el test
file = 'post.xml'

def test_chunk_data():
    assert chunk_data() != []

def test_obtener_datos():
    assert obtener_datos() != []

def test_mapper():
    assert mapper() != []



## Obtiene los datos de los post preguntas. Id, score, creation_date
## arg: data_chunk obtenido 
## return: retorna una tupla con id, score y creatio_date de las preguntas.
def test_obt_score():
    assert obt_score() != []


## Obtiene los datos de los post respuestas. ParenId, CreationDate.
## Arg: Data chunk obtenido.
## Return: Retorna una tupla con dos datos: ParentId y creation_date
def test_obt_parent_date():
    assert obt_parent_date() != []


## Obtiene los datos de las respuestas para analizar
## Arg: Recibe el data_chunk
## Return: Retorna una lista con los datos filtrados
def test_mapper_2():
    assert mapper_2() != []


## Genera una lista de tuplas. Contiene la primer respuesta, la que contiene la fecha mas vieja, la primera en realizarse
## Arg: lista de tuplas con parentId y creationDate ordenadas por el id
## return: genera una lista con la seleccion del parentId mas viejo, el primero en generarse
def test_mapper_3():
    assert mapper_3() != []

def test_reducer(data_1, data_2):
    assert reducer(data_1, data_2) != []


##Compara la lista de datos de pregutnas con la de respuestas para obtener el tiempo que se tarda en responder una pregunta. 
# Suma todos los tiempos para tener el total para las 100 mejors preguntas por score.
## Arg: Lista de tuplas ordenada por id con la fecha de la respuesta.
## Return: Genera un timedelta con la suma de los tiempos que se tardo en responder las 100 mejores preguntas
def test_mapper_4():
    assert mapper_4() != []



## Funcion principal encargada controlar la ejecucion del programa
## Return: Retorna el resultado final.
def test_tiempo_respuesta_promedio():
    assert tiempo_respuesta_promedio() != []


## Ejecuta la funcion principal: tiempo_respuesta_promedio()
## Calula el tiempo desde que comienza la ejecucion hasta que termina.
if __name__=="__main__":

    time_start = time.time()
    logger.info('Comieza la ejecucion del programa')
    tiempo_promedio = tiempo_respuesta_promedio()
    logger.info('Fin del procesamiento de datos')
    time_end = time.time()
    logger.info(f'Tiempo para procesar los datos: {time_end - time_start}')

    logger.info(f'El tiempo de respuesta promedio para las mejores 100 preguntas\n por score es: {tiempo_promedio} ')