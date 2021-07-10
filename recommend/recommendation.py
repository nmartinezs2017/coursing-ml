
import pandas as pd
import os
import sys
from sentence_transformers import util
csfp = os.path.abspath(os.path.dirname(__file__))
if csfp not in sys.path:
    sys.path.insert(0, csfp)
from search import *
from explore import *
from models import *

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

corpus_embeddings_udacity = pd.read_pickle("datasets/model_output/corpus_embeddings_udacity.pkl")
corpus_embeddings_coursera = pd.read_pickle("datasets/model_output/corpus_embeddings_coursera.pkl")
corpus_embeddings_udemy = pd.read_pickle("datasets/model_output/corpus_embeddings_udemy.pkl")


def choose_recommendations_udacity(candidatos_ids, vector_usuario, contexto, description, k):
    # ranking y selección de recomendaciones
    resultados = dict()
    indice = 0

    cursos_ordenados = []
    for candidato_id in candidatos_ids:
        cos_sim = compute_distance_udacity(vector_usuario, int(candidato_id))
        cursos_ordenados.append((candidato_id, cos_sim))

    cursos_ordenados.sort(key=lambda x: x[1])
    cursos_ordenados = cursos_ordenados[::-1]
    candidatos_filtrados = filter_courses(cursos_ordenados, contexto, "udacity")
    c_f_indice = 0
    while(indice < k) and (c_f_indice < len(candidatos_filtrados)):
        c_f_id = candidatos_filtrados[c_f_indice][0]
        related_course = df_ud.iloc[int(c_f_id)]
        # score = content_similarity_udacity(description,related_course['description'])
        resultados[str(c_f_id)] = {'title': related_course['title'], 'url': related_course['url']}
        c_f_indice = c_f_indice + 1
        indice = indice + 1

    return resultados


def choose_recommendations_coursera(candidatos_ids, vector_usuario, contexto, description, k):
    # ranking y selección de recomendaciones
    resultados = dict()
    indice = 0

    cursos_ordenados = []
    for candidato_id in candidatos_ids:
        cos_sim = compute_distance_coursera(vector_usuario, int(candidato_id))
        cursos_ordenados.append((candidato_id, cos_sim))

    cursos_ordenados.sort(key=lambda x: x[1])
    cursos_ordenados = cursos_ordenados[::-1]
    candidatos_filtrados = filter_courses(cursos_ordenados, contexto, "coursera")
    c_f_indice = 0
    while(indice < k) and (c_f_indice < len(candidatos_filtrados)):
        c_f_id = candidatos_filtrados[c_f_indice][0]
        related_course = df_cou.iloc[int(c_f_id)]
        # score = content_similarity_coursera(description, related_course['description'])
        resultados[str(c_f_id)] = {'title': related_course['title'], 'url': related_course['url']}
        c_f_indice = c_f_indice + 1
        indice = indice + 1

    return resultados


def choose_recommendations_udemy(candidatos_ids, vector_usuario, contexto, description, k):
    # ranking y selección de recomendaciones
    resultados = dict()
    indice = 0

    cursos_ordenados = []
    for candidato_id in candidatos_ids:
        cos_sim = compute_distance_udemy(vector_usuario, int(candidato_id))
        cursos_ordenados.append((candidato_id, cos_sim))

    cursos_ordenados.sort(key=lambda x: x[1])
    cursos_ordenados = cursos_ordenados[::-1]
    candidatos_filtrados = filter_courses(cursos_ordenados, contexto, "udemy")
    c_f_indice = 0
    while(indice < k) and (c_f_indice < len(candidatos_filtrados)):
        c_f_id = candidatos_filtrados[c_f_indice][0]
        related_course = df_ude.iloc[int(c_f_id)]
        # score = content_similarity_udemy(description, related_course['description'])
        resultados[str(c_f_id)] = {'title': related_course['title'], 'url': related_course['url']}
        c_f_indice = c_f_indice + 1
        indice = indice + 1

    return resultados


def create_list_recommendations_udacity(perfil, contexto, k, query = ""):
    # buscar cursos que por contenido puedan interesar al usuario
    query_embedding = model_udacity.encode(perfil.description + " " + query, convert_to_tensor=True)
    search_hits = util.semantic_search(query_embedding, corpus_embeddings_udacity, top_k=30)
    search_hits = search_hits[0]
    list_ids = []
    for hit in search_hits:
        list_ids.append(hit['corpus_id'])

    # computar vector de features
    user_embedding = convertir_datos_en_features_udacity(perfil)
  #  df_user = pd.DataFrame([user_embedding], columns=["difficulty", "duration", "n_reviews", "rating", "free"])
    list_recommendations = choose_recommendations_udacity(list_ids, user_embedding, contexto, perfil.description, k)
    return list_recommendations

def create_list_recommendations_coursera(perfil, contexto, k, query = ""):
    # buscar cursos que por contenido puedan interesar al usuario
    query_embedding = model_coursera.encode(perfil.description + " " + query, convert_to_tensor=True)
    search_hits = util.semantic_search(query_embedding, corpus_embeddings_coursera, top_k=k*5)
    search_hits = search_hits[0]
    list_ids = []
    for hit in search_hits:
        list_ids.append(hit['corpus_id'])

    # computar vector de features
    user_embedding = convertir_datos_en_features_coursera(perfil)
    list_recommendations = choose_recommendations_coursera(list_ids, user_embedding, contexto, perfil.description, k)
    return list_recommendations


def create_list_recommendations_udemy(perfil, contexto, k, query = ""):
    # buscar cursos que por contenido puedan interesar al usuario
    query_embedding = model_udemy.encode(perfil.description + " " + query, convert_to_tensor=True)
    search_hits = util.semantic_search(query_embedding, corpus_embeddings_udemy, top_k=k*5)
    search_hits = search_hits[0]
    list_ids = []
    for hit in search_hits:
        list_ids.append(hit['corpus_id'])

    # computar vector de features
    user_embedding = convertir_datos_en_features_udemy(perfil)
    list_recommendations = choose_recommendations_udemy(list_ids, user_embedding, contexto, perfil.description, k)
    return list_recommendations


##### inicialización #####
ss, mms = import_encoders_udacity()
coursera_inst_imputer, coursera_rating_transformer, coursera_inst_encoder, coursera_powertransformer = import_encoders_coursera()
udemy_powertransformer = import_encoders_udemy()