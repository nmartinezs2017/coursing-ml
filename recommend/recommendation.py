from kedro.framework.context.context import load_context
import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
import hdbscan
import os
import sys
from sentence_transformers import util
csfp = os.path.abspath(os.path.dirname(__file__))
if csfp not in sys.path:
    sys.path.insert(0, csfp)
from search import *
from explore import *
from models import *

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

corpus_embeddings_udacity = context.catalog.load("corpus_embeddings_udacity")
corpus_embeddings_coursera = context.catalog.load("corpus_embeddings_coursera")
corpus_embeddings_udemy = context.catalog.load("corpus_embeddings_udemy")

def choose_recommendations_udacity(candidatos_ids, vector_usuario, contexto, k):
    resultados = dict()
    indice = 0

    cursos_ordenados = []
    for candidato_id in candidatos_ids:
        related_course_features = df_cl_ud.iloc[int(candidato_id)]
        rating = related_course_features['rating']
        if (np.isnan(rating)):
            rating = 0
        vector_candidato = [related_course_features['difficulty'], related_course_features['duration'], related_course_features['n_reviews'], rating, related_course_features['free']]
        cos_sim = dot(vector_candidato, vector_usuario)/(norm(vector_candidato)*norm(vector_usuario))
        cursos_ordenados.append((candidato_id, cos_sim))

    cursos_ordenados.sort(key=lambda x: x[1])
    cursos_ordenados = cursos_ordenados[::-1]
    c_f_indice = 0
    while(indice < k) and (c_f_indice < len(cursos_ordenados)):
        c_f_id = cursos_ordenados[c_f_indice][0]
        related_course = df_ud.iloc[int(c_f_id)]
        resultados[str(indice)] = {'id': str(cursos_ordenados[c_f_indice][0]), 'title': related_course['title'], 'url': related_course['url']}
        c_f_indice = c_f_indice + 1
        indice = indice + 1

    return resultados


def choose_recommendations_coursera(candidatos_ids, vector_usuario, contexto, k):
    resultados = dict()
    indice = 0

    cursos_ordenados = []
    for candidato_id in candidatos_ids:
        # related_course = df_ud.iloc[int(candidato_id)]
        related_course_features = df_cl_cou.iloc[int(candidato_id)]
        rating = related_course_features['rating']
        if (np.isnan(rating)):
            rating = 0
        vector_candidato = [related_course_features['difficulty'], related_course_features['total_hours'], related_course_features['enrolled'], rating, related_course_features['institution']]
        cos_sim = dot(vector_candidato, vector_usuario)/(norm(vector_candidato)*norm(vector_usuario))
        cursos_ordenados.append((candidato_id, cos_sim))

    cursos_ordenados.sort(key=lambda x: x[1])
    cursos_ordenados = cursos_ordenados[::-1]
    candidatos_filtrados = filtrar_cursos_coursera(cursos_ordenados, contexto)
    c_f_indice = 0
    while(indice < k) and (c_f_indice < len(candidatos_filtrados)):
        c_f_id = candidatos_filtrados[c_f_indice][0]
        related_course = df_cou.iloc[int(c_f_id)]
        resultados[str(indice)] = {'id': str(candidatos_filtrados[c_f_indice][0]), 'title': related_course['title'], 'url': related_course['url']}
        c_f_indice = c_f_indice + 1
        indice = indice + 1

    return resultados


def choose_recommendations_udemy(candidatos_ids, vector_usuario, contexto, k):
    resultados = dict()
    indice = 0

    cursos_ordenados = []
    for candidato_id in candidatos_ids:
        related_course_features = df_cl_ude.iloc[int(candidato_id)]
        vector_candidato = [related_course_features['cost'], related_course_features['n_students'], related_course_features['rating'], related_course_features['hours']]
        cos_sim = dot(vector_candidato, vector_usuario)/(norm(vector_candidato)*norm(vector_usuario))
        cursos_ordenados.append((candidato_id, cos_sim))

    cursos_ordenados.sort(key=lambda x: x[1])
    cursos_ordenados = cursos_ordenados[::-1]
    candidatos_filtrados = filtrar_cursos_udemy(cursos_ordenados, contexto)
    c_f_indice = 0
    while(indice < k) and (c_f_indice < len(candidatos_filtrados)):
        c_f_id = candidatos_filtrados[c_f_indice][0]
        related_course = df_ude.iloc[int(c_f_id)]
        resultados[str(indice)] = {'id': str(candidatos_filtrados[c_f_indice][0]), 'title': related_course['title'], 'url': related_course['url']}
        c_f_indice = c_f_indice + 1
        indice = indice + 1

    return resultados


def create_list_recommendations_udacity(perfil, contexto, k, query = ""):
    # buscar cursos que por contenido puedan interesar al usuario
    query_embedding = model_udacity.encode(perfil.description + query, convert_to_tensor=True)
    search_hits = util.semantic_search(query_embedding, corpus_embeddings_udacity, top_k=30)
    search_hits = search_hits[0]
    list_ids = []
    for hit in search_hits:
        list_ids.append(hit['corpus_id'])

    # predecir el cluster del user a partir de sus características
    user_embedding = convertir_datos_en_features_udacity(perfil)
  #  df_user = pd.DataFrame([user_embedding], columns=["difficulty", "duration", "n_reviews", "rating", "free"])
    list_recommendations = choose_recommendations_udacity(list_ids, user_embedding, contexto, k)
    return list_recommendations

def create_list_recommendations_coursera(perfil, contexto, k, query = ""):
    # buscar cursos que por contenido puedan interesar al usuario
    query_embedding = model_coursera.encode(perfil.description + query, convert_to_tensor=True)
    search_hits = util.semantic_search(query_embedding, corpus_embeddings_coursera, top_k=100)
    search_hits = search_hits[0]
    list_ids = []
    for hit in search_hits:
        list_ids.append(hit['corpus_id'])

    # predecir el cluster del user a partir de sus características
    user_embedding = convertir_datos_en_features_coursera(perfil)
    list_recommendations = choose_recommendations_coursera(list_ids, user_embedding, contexto, k)
    return list_recommendations


def create_list_recommendations_udemy(perfil, contexto, k, query = ""):
    # buscar cursos que por contenido puedan interesar al usuario
    query_embedding = model_udemy.encode(perfil.description + query, convert_to_tensor=True)
    search_hits = util.semantic_search(query_embedding, corpus_embeddings_udemy, top_k=100)
    search_hits = search_hits[0]
    list_ids = []
    for hit in search_hits:
        list_ids.append(hit['corpus_id'])

    print(list_ids)

    # predecir el cluster del user a partir de sus características
    user_embedding = convertir_datos_en_features_udemy(perfil)
    list_recommendations = choose_recommendations_udemy(list_ids, user_embedding, contexto, k)
    return list_recommendations


##### inicialización #####
ss, mms = import_encoders_udacity()
coursera_inst_imputer, coursera_rating_transformer, coursera_inst_encoder, coursera_powertransformer = import_encoders_coursera()
udemy_powertransformer = import_encoders_udemy()