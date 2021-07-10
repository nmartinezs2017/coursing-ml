
import os
import sys
import pandas as pd
csfp = os.path.abspath(os.path.dirname(__file__))
if csfp not in sys.path:
    sys.path.insert(0, csfp)
from common import *


model_udacity = pd.read_pickle("models/nlp_model_udacity.pkl")
model_coursera = pd.read_pickle("models/nlp_model_coursera.pkl")
model_udemy = pd.read_pickle("models/nlp_model_udemy.pkl")

clustering_model_udacity = pd.read_pickle("models/clustering_model_udacity.pkl")
clustering_model_coursera = pd.read_pickle("models/clustering_model_coursera.pkl")
clustering_model_udemy = pd.read_pickle("models/clustering_model_udemy.pkl")

df_ud = pd.read_csv("datasets/cleaned_udacity.csv")
df_cou = pd.read_csv("datasets/cleaned_coursera.csv")
df_ude = pd.read_csv("datasets/cleaned_udemy.csv")

df_cl_ud = pd.read_csv("datasets/model_output/clustering_output_udacity.csv")
df_cl_cou = pd.read_csv("datasets/model_output/clustering_output_coursera.csv")
df_cl_ude = pd.read_csv("datasets/model_output/clustering_output_udemy.csv")


def explore_courses_udacity(perfil, contexto, k):
    # crear feature usuario udacity
    feature_usuario = convertir_datos_en_features_udacity(perfil)
    # buscar su cluster
    cluster_id = predecir_cluster_udacity(feature_usuario)
    # crear lista de recomendaciones
    list_id_courses = df_cl_ud[df_cl_ud['Label'] == cluster_id].index.tolist()
    cursos_candidatos = []
    for id_course in list_id_courses:
        curso = get_curso_udacity(int(id_course))
        if (not pd.isnull(curso.description)):
            cos_sim = content_similarity_udacity(perfil.description, curso.description)
            cursos_candidatos.append((id_course, cos_sim))
    # filtrar
    cursos_filtrados = filter_courses(cursos_candidatos, contexto, "udacity")
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
    # crear lista de recomendaciones
    list_id_courses = df_cl_cou[df_cl_cou['Label'] == cluster_id].index.tolist()
    cursos_candidatos = []
    for id_course in list_id_courses:
        curso = get_curso_coursera(int(id_course))
        if (not pd.isnull(curso.description)):
            cos_sim = content_similarity_coursera(perfil.description, curso.description)
            cursos_candidatos.append((id_course, cos_sim))
    # filtrar
    cursos_filtrados = filter_courses(cursos_candidatos, contexto, "coursera")
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
    # crear lista de recomendaciones
    list_id_courses = df_cl_ude[df_cl_ude['Label'] == cluster_id].index.tolist()
    cursos_candidatos = []
    for id_course in list_id_courses:
        curso = get_curso_udemy(int(id_course))
        curso_descripcion = curso.description + ". " + curso.description_extend
        if (not pd.isnull(curso.description)):
            cos_sim = content_similarity_udemy(perfil.description, curso_descripcion)
            cursos_candidatos.append((id_course, cos_sim))
    # filtrar
    cursos_filtrados = filter_courses(cursos_candidatos, contexto, "udemy")
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