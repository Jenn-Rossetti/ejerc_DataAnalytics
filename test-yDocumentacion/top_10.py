"""
Utilizar MapReduce para el grupo de datos E
* Top 10 fechas con mayor cantidad de post creados
"""

from functools import reduce
from typing import Counter
import xml.etree.ElementTree as ET
import logging
import logging.config
import time
import datetime
import os, sys


ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#ruta_include = path.abspath(path.join(ruta_base, 'include'))
try:
    logging.config.fileConfig(f'{ruta_base}/data_group_E/logging.cfg')
    
    # create logger
    logger = logging.getLogger('top_10')
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

def obtener_datos():

    try:
        post = ET.parse(f"{ruta_base}/data_set/112010 Meta Stack Overflow/posts.xml")
        data_post = post.getroot()
        logger.info('Datos obtenidos con exito.')
        return data_post
    except FileNotFoundError as e:
        logger.error("Archivo de datos no encontrado en la ruta.")
        raise FileNotFoundError(f"Error al obtener los datos: {e} ")
    except Exception as e:
        logger.error(e)
        raise e
    



def chunk_data(iterable, len_of_chunk):

    try:
        if len_of_chunk < 0:
            raise TypeError('El numero de len_of_chunk debe ser mayor a 0')
        resultado = [iterable[i:i + len_of_chunk] for i in range(0, len(iterable), len_of_chunk)]
        logger.info('Datos separados en partes con exito')
        return resultado
    except TypeError as e:
        logger.error(f"Ocurrió una excepción identificada: {e}")
    


def obtener_fechas(data):

    try:
        fechas = data.attrib['CreationDate']
        fecha_formateada = datetime.datetime.strptime(fechas, '%Y-%m-%dT%H:%M:%S.%f')
        fecha_formateada = fecha_formateada.strftime('%Y-%m-%d')
        
        return fecha_formateada
    except Exception as e:
        logger.error(f'Error en la obtencion de las fechas: {e}')

def suma_fechas(data1, data2):
    
    data1.update(data2)
    return data1

def mapper(data):

    fechas_mapeadas = list(map(obtener_fechas, data))
    counter_fecha = Counter(fechas_mapeadas)
    return counter_fecha


def top_10_post_por_fecha():

    try:
        data = obtener_datos()
        data_chuncks = chunk_data(data, 50)
        mapped = list(map(mapper, data_chuncks))
        logger.info('Fechas obtenidas y formateadas con exito')
        top_10 = reduce(suma_fechas, mapped).most_common(10)
        logger.info('Cantidad total de post por fechas obtenidos y seleccionado el top 10')
        return top_10
    except Exception as e:
        logger.error(f'Errro en la ejecucion de top_10_post_por_fecha. {e} ')


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