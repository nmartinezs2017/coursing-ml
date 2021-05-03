import math
import os
import sys
from numpy import dot
from numpy.linalg import norm
import pandas as pd
import numpy as np
csfp = os.path.abspath(os.path.dirname(__file__))
if csfp not in sys.path:
    sys.path.insert(0, csfp)
from common import *
from kedro.framework.context import load_context
from sentence_transformers import util
context = load_context('../coursing-ml/')
model_udacity = context.catalog.load("nlp_model_udacity")
model_coursera = context.catalog.load("nlp_model_coursera")
df_cl_ud = context.catalog.load("clustering_output_udacity")
df_cl_cou = context.catalog.load("clustering_output_coursera")
df_ud = context.catalog.load("cleaned_udacity")
df_cou = context.catalog.load("cleaned_coursera")


def calcular_contenido_similitud_udacity(perfil, curso_id):
    print(curso_id)
    curso = df_cl_ud.iloc[curso_id]
    usuario_embedding = convertir_datos_en_features_udacity(perfil)
    rating = curso['rating']
    if (np.isnan(rating)):
        rating = 0
    curso_embedding = [curso['difficulty'], curso['duration'], curso['n_reviews'], rating, curso['free']]
    print(curso_embedding)
    print(usuario_embedding)
    cos_sim = dot(curso_embedding, usuario_embedding) / (norm(curso_embedding) * norm(usuario_embedding))
    print(cos_sim)
    return cos_sim


def calcular_contenido_similitud_coursera(perfil, curso_id):
    curso = df_cl_cou.iloc[curso_id]
    usuario_embedding = convertir_datos_en_features_coursera(perfil)
    rating = curso['rating']
    if (np.isnan(rating)):
        rating = 0
    curso_embedding = [curso['difficulty'], curso['total_hours'], curso['enrolled'], rating, curso['institution']]
    cos_sim = dot(curso_embedding, usuario_embedding) / (norm(curso_embedding) * norm(usuario_embedding))
    return cos_sim


def filtrar_cursos(cursos_candidatos, contexto):
    resultado = []
    for candidato_id, score in cursos_candidatos:
        curso_candidato = get_curso_coursera(candidato_id)
        idioma_correcto = curso_candidato.language in contexto.lista_idiomas
        nuevo_contenido = candidato_id not in contexto.cursos_descartados
        if idioma_correcto and nuevo_contenido:
            resultado.append((candidato_id, score))
    return resultado


def explore_courses_udacity(perfil, contexto, k):
    # crear feature usuario udacity
    feature_usuario = convertir_datos_en_features_udacity(perfil)
    # buscar su cluster
    cluster_id = predecir_cluster_udacity(feature_usuario)
    # crear lista
    list_id_courses = df_cl_ud[df_cl_ud['Label'] == cluster_id].index.tolist()
    cursos_candidatos = []
    for id_course in list_id_courses:
        curso = df_ud.iloc[int(id_course)]
        if (not pd.isnull(curso.description)):
            cos_sim = calcular_contenido_similitud_udacity(perfil, id_course)
            cursos_candidatos.append((id_course, cos_sim))
    # filtrar
    print(cursos_candidatos)
    cursos_filtrados = filtrar_cursos(cursos_candidatos, contexto)
    print(cursos_candidatos)
    # ordenar
    cursos_filtrados.sort(key=lambda x: x[1])
    # devolver los k primeros
    indice = 0
    resultados = dict()
    while (indice < k) and (indice < len(cursos_filtrados)):
        id_course, _ = cursos_filtrados[indice]
        related_course = df_ud.iloc[id_course]
        resultados[id_course] = {'title': related_course['title'], 'url': related_course['url']}
        indice = indice + 1

    return resultados

def explore_courses_coursera(perfil, contexto, k):
    # crear feature usuario udacity
    feature_usuario = convertir_datos_en_features_coursera(perfil)
    # buscar su cluster
    cluster_id = predecir_cluster_coursera(feature_usuario)
    # crear lista
    list_id_courses = df_cl_cou[df_cl_cou['Label'] == cluster_id].index.tolist()
    cursos_candidatos = []
    for id_course in list_id_courses:
        curso = df_cou.iloc[int(id_course)]
        if (not pd.isnull(curso.description)):
            cos_sim = calcular_contenido_similitud_coursera(perfil, id_course)
            cursos_candidatos.append((id_course, cos_sim))
    # filtrar
    cursos_filtrados = filtrar_cursos(cursos_candidatos, contexto)
    # ordenar
    cursos_filtrados.sort(key=lambda x: x[1])
    # devolver los k primeros
    indice = 0
    resultados = dict()
    while (indice < k) and (indice < len(cursos_filtrados)):
        id_course, _ = cursos_filtrados[indice]
        related_curso = df_cou.iloc[id_course]
        resultados[id_course] = {'title': related_curso['title'], 'url': related_curso['url']}
        indice = indice + 1

    return resultados