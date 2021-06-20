import math
import os
import sys
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
model_udemy = context.catalog.load("nlp_model_udemy")

clustering_model_udacity = context.catalog.load("clustering_model_udacity")
clustering_model_coursera = context.catalog.load("clustering_model_coursera")
clustering_model_udemy = context.catalog.load("clustering_model_udemy")

df_ud = context.catalog.load("cleaned_udacity")
df_cou = context.catalog.load("cleaned_coursera")
df_ude = context.catalog.load("cleaned_udemy")

df_cl_ud = context.catalog.load("clustering_output_udacity")
df_cl_cou = context.catalog.load("clustering_output_coursera")
df_cl_ude = context.catalog.load("clustering_output_udemy")


def explore_courses_udacity(perfil, contexto, k):
    # crear feature usuario udacity
    feature_usuario = convertir_datos_en_features_udacity(perfil)
    # buscar su cluster
    cluster_id = predecir_cluster_udacity(feature_usuario)
    # crear lista
    list_id_courses = df_cl_ud[df_cl_ud['Label'] == cluster_id].index.tolist()
    cursos_candidatos = []
    for id_course in list_id_courses:
        curso = get_curso_udacity(int(id_course))
        if (not pd.isnull(curso.description)):
            cos_sim = calcular_similitud_contenido_udacity(perfil.description, curso.description)
            cursos_candidatos.append((id_course, cos_sim))
    # ordenar
    cursos_candidatos.sort(key=lambda x: x[1])
    # devolver los k primeros
    indice = 0
    resultados = dict()
    while (indice < k) and (indice < len(cursos_candidatos)):
        id_course, _ = cursos_candidatos[indice]
        related_course = df_ud.iloc[id_course]
        resultados[id_course] = {'id': id_course, 'title': related_course['title'], 'url': related_course['url']}
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
        curso = get_curso_coursera(int(id_course))
        if (not pd.isnull(curso.description)):
            cos_sim = calcular_similitud_contenido_coursera(perfil.description, curso.description)
            cursos_candidatos.append((id_course, cos_sim))
    # filtrar
    cursos_filtrados = filtrar_cursos_coursera(cursos_candidatos, contexto)
    # ordenar
    cursos_filtrados.sort(key=lambda x: x[1])
    # devolver los k primeros
    indice = 0
    resultados = dict()
    while (indice < k) and (indice < len(cursos_filtrados)):
        id_course, _ = cursos_filtrados[indice]
        related_curso = df_cou.iloc[id_course]
        resultados[id_course] = {'id': id_course, 'title': related_curso['title'], 'url': related_curso['url']}
        indice = indice + 1

    return resultados


def explore_courses_udemy(perfil, contexto, k):
    # crear feature usuario udemy
    feature_usuario = convertir_datos_en_features_udemy(perfil)
    # buscar su cluster
    cluster_id = predecir_cluster_udemy(feature_usuario)
    # crear lista
    list_id_courses = df_cl_ude[df_cl_ude['Label'] == cluster_id].index.tolist()
    cursos_candidatos = []
    for id_course in list_id_courses:
        curso = get_curso_udemy(int(id_course))
        curso_descripcion = curso.description + ". " + curso.description_extend
        if (not pd.isnull(curso.description)):
            cos_sim = calcular_similitud_contenido_udemy(perfil.description, curso_descripcion)
            cursos_candidatos.append((id_course, cos_sim))
    # filtrar
    print(cursos_candidatos)
    cursos_filtrados = filtrar_cursos_udemy(cursos_candidatos, contexto)
    print(cursos_filtrados)
    # ordenar
    cursos_filtrados.sort(key=lambda x: x[1])
    # devolver los k primeros
    indice = 0
    resultados = dict()
    while (indice < k) and (indice < len(cursos_filtrados)):
        id_course, _ = cursos_filtrados[indice]
        related_curso = df_ude.iloc[id_course]
        resultados[id_course] = {'id': id_course, 'title': related_curso['title'], 'url': related_curso['url']}
        indice = indice + 1

    return resultados