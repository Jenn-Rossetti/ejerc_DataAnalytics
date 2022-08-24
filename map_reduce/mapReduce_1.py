
from ast import parse
import xml.etree.ElementTree as Elt
import xml.etree.ElementTree as ET
import pandas as pd
import operator
import logging
import logging.config
from datetime import datetime as dt
from functools import reduce
from typing import List, Tuple
import timeit

#COMO: Analista de datos
#QUIERO: Utilizar MapReduce
#PARA: Analizar los datos de StackOverflow

logging.config.fileConfig('./config/logging.cfg')
file_logger = logging.getLogger('fileRotating')
console_logger = logging.getLogger('console')


xml_path1 = './Stack Overflow 11-2010/112010 Meta Stack Overflow/posts.xml'
csv_name1 = './xlmtocsv.csv'

def analizador(xml_path: str):
    tree = Elt.parse(xml_path)
    return tree


# 1) Top 10 fechas con mayor cantidad de post creados

def chunkify(file, chunk_len): 
    tree = ET.parse(file)
    data = tree.getroot()
    chunks = [data[i:i + chunk_len] for i in range(0, len(data), chunk_len)]
    return chunks


def mapper(data):
    #se lee el archivo xml que contiene los datos
    tag_list = []
    
    for node in data.iter('row'):
        tags = node.attrib.get('Tags')
        AcceptedAnswer = node.attrib.get('AcceptedAnswerId')
        #se comprubea si es un tag valido y si no tiene respuestas aceptadas
        if AcceptedAnswer == None and tags != None:
            #si se cumplen las condiciones se agrega el tag a la lista
            tag_list.append(tags)
    return tag_list

def reducer(data):
    reducer = {}
    #se itera por cada tag que hay en la lista
    for n in data:
        if n in reducer:
            reducer[n] += 1
        else:
            reducer[n] = 1  
    reducer = sorted(reducer.items(), key=operator.itemgetter(1), reverse=True)
    #se extrae los 10 primeros valores de la lista
    reducer = reducer[:10]
    return reducer

if __name__ == "__main__":
    try:
        data = chunkify('post.xml')
    except FileNotFoundError as e:
        print('error al abrir el archivo')
    else:
        datamaped = mapper(data)
        print(reducer(datamaped))


#-------------------------------------


 # 2)Relación entre cantidad de respuestas y sus visitas.

 # Definición de la función de mapeo principal que devuelve el Id, AnswerCount Tuples
def mapper_func(row_obj: Elt.Element):
    if row_obj.attrib['PostTypeId'] == '1':
        if 'AnswerCount' in row_obj.attrib.keys():
            answer_count = int(row_obj.attrib['AnswerCount'])
        else:
            answer_count = 0
        return (row_obj.attrib['Id'], answer_count)
    else:
        pass


# Definición de la función para luego ordenar los datos por su cantidad de AnswerCount.
def sorter_func(tuple1: Tuple, tuple2: Tuple):
    if tuple2[1] > tuple1[1]:
        return tuple2
    else:
        return tuple1



#definimos entradas mas respondidas
def mas_respondidas(list_of_tuples: List):
    mas_respondidas = []
    for i in range(10):
        id_max_answer = reduce(sorter_func, list_of_tuples)
        mas_respondidas.append(id_max_answer)
        max_id = id_max_answer[0]

        def max_value_popper(tuple1: Tuple):
            if tuple1[0] == max_id:
                return False
            else:
                return True
        list_of_tuples = list(filter(max_value_popper, list_of_tuples))
    return mas_respondidas

def main_mapper_func(
    list_test: List,
):
    id_answers_mapped = list(map(mapper_func, list_test))
    id_answers_clean = list(filter(None, id_answers_mapped))
    max_list = mas_respondidas(id_answers_clean)
    return max_list

def red_cleaning_func(list1: List, list2: List):
    list3 = list1 + list2
    return list3


# asigna, reduce y devuelve el resultado deseado.
def rendimiento():
    list_of_chunks = chunkify(parse(xml_path1), 6)
    max_list = list(map(main_mapper_func, list_of_chunks))
    max_list_clean = reduce(red_cleaning_func, max_list)
    list_of_chunks.close()
    top_10_max = mas_respondidas(max_list_clean)
    num = 1
    message = ''
    for item in top_10_max:
        message += (f'{num}) PostId: {item[0]} Answers: {item[1]}\n')
        num += 1
    file_logger.info(f' Las publicaciones más respondidas son:\n{message}')
    console_logger.info(f' Las publicaciones más respondidas son:\n{message}')
    return

rendimiento()

 # 3) Del ranking de los primeros 0-100 por score, tomar el tiempo de respuesta promedio e informar un único valor

tiempo = timeit.timeit('tag_list = [i for i in range(100)]', number=1)
# Calculamos el tiempo medio
print(tiempo)