"""
Utilizar MapReduce para el grupo de datos E
* Del ranking de los primeros 0-100 por score, tomar el tiempo 
  de respuesta promedio e informar un único valor.
"""


from functools import reduce

import xml.etree.ElementTree as ET
import logging
import logging.config
import time
from datetime import datetime
from datetime import timedelta
import os


ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
try:
    logging.config.fileConfig(f'{ruta_base}/data_group_E/logging.cfg')
    # create logger
    logger = logging.getLogger('Tiempo_Respuesta_promedio')
    """
    # application code for logger
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')
    """
except KeyError as e:
   print('No se encontro el archivo logging.cfg en el path especificado.')
   raise e
except FileNotFoundError as e:
    print(f'La ruta el directorio es incorrecta. {e}')
    raise e

def chunk_data(iterable, len_of_chunk):

    try:
        if len_of_chunk < 0:
            raise TypeError('El numero de len_of_chunk debe ser mayor a 0')
        for i in range(0, len(iterable), len_of_chunk):
            yield iterable[i:i +len_of_chunk]
        
    except TypeError as e:
        logger.error(f"Ocurrió una excepción identificada: {e}")


def obtener_datos():

    try:
        post = ET.parse(f"{ruta_base}/data_set/112010 Meta Stack Overflow/posts.xml")
        data_post = post.getroot()
        
        return data_post
    except FileNotFoundError as e:
        logger.error("Archivo de datos no encontrado en la ruta.")
        raise FileNotFoundError(f"Error al obtener los datos: {e} ")
    except Exception as e:
        logger.error(e)
        raise e

def obt_score(data):

    try:
        PostTypeId = data.attrib['PostTypeId']
        if PostTypeId == '1':
            id = data.attrib['Id']
            score = int(data.attrib['Score'])
            creation_date = data.attrib['CreationDate']
            creation_date = datetime.strptime(creation_date, '%Y-%m-%dT%H:%M:%S.%f')
            return id, score, creation_date

    except Exception as e:
        logger.error(f'Error al obtener los datos de las preguntas.  {e}')
        raise e

def obt_parent_date(data):

    try:
        post_type_id = data.attrib['PostTypeId']
        if post_type_id == '2':
            parent_id = data.attrib['ParentId']
            creation_date = data.attrib['CreationDate']
            creation_date = datetime.strptime(creation_date, '%Y-%m-%dT%H:%M:%S.%f')
            return parent_id, creation_date
    except Exception as e:
        logger.error(f'Error al obtener parent_id y creation_date {e}')
        raise e

def mapper(data):

    post_score = list(map(obt_score, data))
    post_score = list(filter(None, post_score))
    return post_score

def mapper_2(data):

    parent_date = list(map(obt_parent_date, data))
    parent_date = list(filter(None, parent_date))
    return parent_date

lista_2 = []
clave = '0'
def mapper_3(data):

    global clave
    for i in data:
        if isinstance(i, str) and clave != i:
            clave = i
            lista_2.append(data)   


def reducer(data_1, data_2):
    data_1 = data_1 + data_2
    return data_1

diferencia = timedelta(seconds=0)
def mapper_4(data):

    try:
        for i in order_score:
            for a in data:
                if i[0] == a:
                    global diferencia
                    diferencia += data[1] - i[2]
    except Exception as e:
        logger.error(f'Error al cruzar datos de preguntas y respuestas: {e}')
        raise e


def tiempo_respuesta_promedio():

    try:
        # Face de Preguntas
        data = obtener_datos()
        data_chuncks = chunk_data(data, 50)
        mapped = list(map(mapper, data_chuncks))
        mapped = reduce(reducer, mapped)
        logger.info('Post con preguntas y score obtenidos con exito.')
        global order_score
        order_score = sorted(mapped, key=lambda x: x[1],reverse=True)[:100]
        logger.info('Mejores 100 score de preguntas procesados y ordenados')

        # Face de Respuestas
        data = obtener_datos()
        data_chuncks = chunk_data(data, 50)
        mapped_2 = list(map(mapper_2, data_chuncks))
        mapped_2 = sorted(reduce(reducer, mapped_2),key=lambda x :x[0])
        logger.info('Datos de respuestas obtenidos con exito')
        list(map(mapper_3, mapped_2))
        logger.info('Datos de respuestas procesados con exito')
        # genera diferencias, devuelve lista: demora
        list(map(mapper_4, lista_2))
        promedio_tiempo_respuesta = diferencia/100
        logger.info('Tiempos de respuestas para los mejores 100 score obtenidos, promedio calculado')

        return promedio_tiempo_respuesta
    except Exception as e:
        logger.error(f'Errro en la ejecucion de tiempo_respuesta_promedio(). {e} ')

if __name__=="__main__":
    """
    Ejecuta la funcion principal: tiempo_respuesta_promedio()
    Calula el tiempo desde que comienza la ejecucion hasta que termina.
    """
    time_start = time.time()
    logger.info('Comieza la ejecucion del programa')
    tiempo_promedio = tiempo_respuesta_promedio()
    logger.info('Fin del procesamiento de datos')
    time_end = time.time()
    logger.info(f'Tiempo para procesar los datos: {time_end - time_start}')

    logger.info(f'El tiempo de respuesta promedio para las mejores 100 preguntas\n por score es: {tiempo_promedio} ')