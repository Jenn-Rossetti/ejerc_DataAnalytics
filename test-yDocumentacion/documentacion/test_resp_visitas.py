## Relación entre cantidad de respuestas y sus visitas

from resp_visitas import obt_views_answer, reducir_views_answer, respuestas_y_visitas
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



## Obtiene los datos de los atributos 'ViewCount' y 'AnswerCout'
## Arg: Datos obtenidos del repositorio
## Return: retorna los datos en forma de enteros, de view y answer
def test_obt_views_answer():
    assert obt_views_answer() != []


## Reduce los resultados sumandolos
## Arg: Recibe dos tuplas que se suman entre si. Cada una tiene 2 enteros.
## Return: Retorna una tupla con la suma de los dos primero numero y los dos segundos
def test_reducir_views_answer(data1, data2):
    assert reducir_views_answer(data1, data2) != []


## Funcion principal encargada controlar la ejecucion del programa
## Return: Retorna el resultado final de visitas y respuestas.
def test_respuestas_y_visitas():
    assert respuestas_y_visitas() != []


## Ejecuta la funcion principal: respuestas_y_visitas()
## Calula el tiempo desde que comienza la ejecucion hasta que termina.
if __name__=="__main__":

    time_start = time.time()
    logger.info('Comieza la ejecucion del programa')
    relacion = respuestas_y_visitas()
    logger.info('Fin del procesamiento de datos')
    time_end = time.time()
    logger.info(f'Tiempo para procesar los datos: {time_end - time_start}')

    logger.info(f'Se obtuvieron {relacion[0]} visitas y {relacion[1]} respuestas en los datos analizados')
    a = relacion[0]/relacion[1]
    logger.info(f'En ralacion, se genera 1 respuesta cada {round(a,2)} visitas')