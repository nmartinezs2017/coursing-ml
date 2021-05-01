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
clustering_model_udacity = context.catalog.load("clustering_model_udacity")
clustering_model_coursera = context.catalog.load("clustering_model_coursera")
df_ud = context.catalog.load("cleaned_udacity")
df_cou = context.catalog.load("cleaned_coursera")
corpus_embeddings_udacity = context.catalog.load("corpus_embeddings_udacity")
corpus_embeddings_coursera = context.catalog.load("corpus_embeddings_coursera")
df_cl_ud = context.catalog.load("clustering_output_udacity")
df_cl_cou = context.catalog.load("clustering_output_coursera")


def escoger_recomendaciones_udacity(candidatos, cluster_id, vector_usuario):
    resultados = dict()
    indice = 0
    for (candidato_id, score_candidato) in candidatos.items():
        related_course = df_ud.iloc[int(candidato_id)]
        related_course_features = df_cl_ud.iloc[int(candidato_id)]
        c_id_candidato = related_course_features['Label']
        if (c_id_candidato == cluster_id):
            resultados[indice] = {'course_id': candidato_id, 'title': related_course['title'], 'url': related_course['url']}
            indice = indice + 1

    candidatos_filtrados = []
    for (candidato_id, score_candidato) in candidatos.items():
        # related_course = df_ud.iloc[int(candidato_id)]
        related_course_features = df_cl_ud.iloc[int(candidato_id)]
        c_id_candidato = related_course_features['Label']
        if (c_id_candidato != cluster_id):
            rating = related_course_features['rating']
            if (np.isnan(rating)):
                rating = 0
            vector_candidato = [related_course_features['difficulty'], related_course_features['duration'], related_course_features['n_reviews'], rating, related_course_features['free']]
            cos_sim = dot(vector_candidato, vector_usuario)/(norm(vector_candidato)*norm(vector_usuario))
            candidatos_filtrados.append((candidato_id, cos_sim))

    candidatos_filtrados.sort(key=lambda x: x[1])
    candidatos_filtrados = candidatos_filtrados[::-1]
    c_f_indice = 0
    while(indice < 10) and (c_f_indice < len(candidatos_filtrados)):
        c_f_id = candidatos_filtrados[c_f_indice][0]
        related_course = df_ud.iloc[int(c_f_id)]
        resultados[indice] = {'course_id': candidatos_filtrados[c_f_indice][0], 'title': related_course['title'], 'url': related_course['url']}
        c_f_indice = c_f_indice + 1
        indice = indice + 1

    return resultados


def escoger_recomendaciones_coursera(candidatos, cluster_id, vector_usuario):
    resultados = dict()
    indice = 0
    temp_list = []
    print(cluster_id)
    for key, value in candidatos.items():
        temp = [key, value]
        temp_list.append(temp)

    temp_list.sort(key=lambda x: x[1])
    temp_list = temp_list[::-1]

    for (candidato_id, score_candidato) in temp_list:
        related_course = df_cou.iloc[int(candidato_id)]
        related_course_features = df_cl_cou.iloc[int(candidato_id)]
        c_id_candidato = related_course_features['Label']
        if (c_id_candidato == cluster_id):
            resultados[indice] = {'course_id': candidato_id, 'title': related_course['title'], 'url': related_course['url']}
            indice = indice + 1
            if (indice==10):
                print("Ha llegado al limite")
                break

    candidatos_filtrados = []
    for (candidato_id, score_candidato) in candidatos.items():
        # related_course = df_ud.iloc[int(candidato_id)]
        related_course_features = df_cl_cou.iloc[int(candidato_id)]
        c_id_candidato = related_course_features['Label']
        if (c_id_candidato != cluster_id):
            rating = related_course_features['rating']
            if (np.isnan(rating)):
                rating = 0
            vector_candidato = [related_course_features['difficulty'], related_course_features['total_hours'], related_course_features['enrolled'], rating, related_course_features['institution']]
            cos_sim = dot(vector_candidato, vector_usuario)/(norm(vector_candidato)*norm(vector_usuario))
            candidatos_filtrados.append((candidato_id, cos_sim))

    candidatos_filtrados.sort(key=lambda x: x[1])
    candidatos_filtrados = candidatos_filtrados[::-1]
    c_f_indice = 0
    while(indice < 10) and (c_f_indice < len(candidatos_filtrados)):
        c_f_id = candidatos_filtrados[c_f_indice][0]
        related_course = df_cou.iloc[int(c_f_id)]
        resultados[indice] = {'course_id': candidatos_filtrados[c_f_indice][0], 'title': related_course['title'], 'url': related_course['url']}
        c_f_indice = c_f_indice + 1
        indice = indice + 1

    return resultados

def crear_lista_recomendaciones_udacity(perfil):
    query_embedding = model_udacity.encode(perfil.description, convert_to_tensor=True)

    search_hits = util.semantic_search(query_embedding, corpus_embeddings_udacity, top_k=30)
    search_hits = search_hits[0]

    results = dict()
    for hit in search_hits:
        # related_course = df_ud.iloc[hit['corpus_id']]
        results[str(hit['corpus_id'])] = float(hit['score'])

    row_user = convertir_datos_en_features_udacity(perfil)
    df_user = pd.DataFrame([row_user], columns=["difficulty", "duration", "n_reviews", "rating", "free"])

    labels = clustering_model_udacity.predict(df_user)
    cluster_id = labels[0]
    list_recommendations = escoger_recomendaciones_udacity(results, cluster_id, row_user)
    return list_recommendations

def crear_lista_recomendaciones_coursera(perfil: PerfilUsuario):
    query_embedding = model_coursera.encode(perfil.description, convert_to_tensor=True)

    search_hits = util.semantic_search(query_embedding, corpus_embeddings_coursera, top_k=100)
    search_hits = search_hits[0]

    results = dict()
    for hit in search_hits:
        # related_course = df_ud.iloc[hit['corpus_id']]
        results[str(hit['corpus_id'])] = float(hit['score'])

    row_user = convertir_datos_en_features_coursera(perfil)
    df_user = pd.DataFrame([row_user], columns=["difficulty", "total_hours", "enrolled", "rating", "institution"])

    labels, _ = hdbscan.approximate_predict(clustering_model_coursera, df_user)
    cluster_id = labels[0]
    list_recommendations = escoger_recomendaciones_coursera(results, cluster_id, row_user)
    return list_recommendations


##### inicialización #####
ss, mms = importar_encoders_udacity()
coursera_inst_imputer, coursera_rating_transformer, coursera_inst_encoder, coursera_powertransformer = importar_encoders_coursera()
