## Top 10 fechas con mayor cantidad de post creados

from top_10 import obtener_datos, chunk_data, obtener_fechas, suma_fechas, mapper, top_10_post_por_fecha
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





## Lee los datos desde un archivo externo
## Return: retorna los datos que seran procesados luego
def test_obtener_datos():
    assert obtener_datos(file,10) != []


## Se divide la data en partes para poder trabajarla
## arg: iterable: lista de datos obtenida
    # len_of_chunk: cantidad de partes en las que se dividira la lista
    # retunr: Retorna la lista dividida en partes
def test_chunk_data():
    assert chunk_data() != []


## Obtiene las fechas de creacion de los post desde: CreationDate.
## Luego se formatea la fecha para que retorne Año, Mes, Dia
## Return: Retorna las fechas formateadas.
def test_obtener_fechas():
    assert obtener_fechas() != []


## Se realiza un update a cada Counter para sumar la cantidad de post que hay por fecha
def test_suma_fechas():
    assert suma_fechas() != []


##  Primero se obtine la lista de fechas en las que hay un post.
## Luego, mediante el Counter, se devuelve la suma de todas las fechas que tienen post
## Arg: data: Info obtenida y dividida partes
## Return: Retorna todas las fechas, con la cantidad de post que se hicieron en esa fecha
def test_mapper():
    assert mapper() != []



## Funcion principal: ejecuta la obtencion de la data.
## Ejecuta al divicion de la data en 50 partes, medianta data_chuncks.
## Se mapea el data_chuncks para procesar los datos.
## Se hace un reduce para sumar los datos y obtener el top_10
## Return: Retorna el top 10 de fechas con mas post
def test_top_10_post_por_fecha():
    assert top_10_post_por_fecha() != []


## Ejecuta la funcion principal: top_10_post_por_fecha()
## Calula el tiempo deade que comienza la ejecucion hasta que termina.
if __name__=="__main__":

    time_start = time.time()
    logger.info('Comiena la ejecucion del programa')
    top = top_10_post_por_fecha()
    logger.info('Fin de la ejecucion')
    time_end = time.time()

    logger.info(f'El top 10 fechas con mayor cantidad de post es:\n')
    for i in top:
        logger.info(f'En la fecha: {i[0]} se crearon => {i[1]} posts')
    
    logger.info(f'Tiempo para procesar los datos: {time_end - time_start}')