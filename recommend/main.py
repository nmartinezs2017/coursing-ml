import os
import pickle
import sys
import hdbscan
from fastapi import FastAPI
from typing import Optional, List
import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
from pydantic import BaseModel
from sentence_transformers import util
# csfp - current_script_folder_path

csfp = os.path.abspath(os.path.dirname(__file__))
if csfp not in sys.path:
    sys.path.insert(0, csfp)
# import it and invoke it by one of the ways described above
from search import *
from models import PerfilUsuarioUdacity, PerfilUsuarioCoursera, ContextoUsuarioBusqueda
from kedro.framework.context.context import load_context

app = FastAPI()

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


@app.get("/")
def read_root():
    return {"Hello": "World"}


def importar_encoders_udacity():
    pkl_file = open('encoders_coursera.pkl', 'rb')
    encoders_dict = pickle.load(pkl_file)
    pkl_file.close()
    ss = encoders_dict["udacity_duration_ss"]
    mms = encoders_dict["udacity_rating_mms"]
    return ss, mms


def importar_encoders_coursera():
    pkl_file = open('encoders_coursera.pkl', 'rb')
    coursera_encoders_dict = pickle.load(pkl_file)
    coursera_inst_imputer = coursera_encoders_dict["coursera_inst_imputer"]
    coursera_rating_transformer = coursera_encoders_dict["coursera_rating_transformer"]
    coursera_inst_encoder = coursera_encoders_dict["coursera_inst_encoder"]
    coursera_powertransformer = coursera_encoders_dict["coursera_powertransformer"]
    pkl_file.close()
    return coursera_inst_imputer, coursera_rating_transformer, coursera_inst_encoder, coursera_powertransformer


def convertir_datos_en_features_coursera(perfil: PerfilUsuarioCoursera):
    if (perfil.difficulty == 'beginner'):
        user_difficulty = 0
    elif (perfil.difficulty == 'intermediate'):
        user_difficulty = 1
    else:
        user_difficulty = 2
    df_user = pd.DataFrame([[user_difficulty, perfil.duration, perfil.n_reviews, perfil.rating, perfil.institution]], columns=["difficulty","total_hours","enrolled", "rating", "institution"])
    df_user = coursera_rating_transformer.transform(df_user)
    numerical_features = ['difficulty', 'total_hours', 'enrolled', 'rating']
    df_user[numerical_features] = coursera_powertransformer.transform(df_user[numerical_features])
    df_user = coursera_inst_encoder.transform(df_user)
    print(df_user)
    return df_user.iloc[0].to_numpy()


def convertir_datos_en_features_udacity(perfil: PerfilUsuarioUdacity):
    if (perfil.difficulty == 'beginner'):
        user_difficulty = 0
    elif (perfil.difficulty == 'intermediate'):
        user_difficulty = 1
    else:
        user_difficulty = 2
    user_duration = ss.transform([[perfil.duration]])
    user_free = perfil.free
    user_popularity = 0
    user_rating = mms.transform([[perfil.rating]])

    return [user_difficulty, user_duration[0][0], user_popularity, user_rating[0][0], user_free]


def escoger_recomendaciones_udacity(candidatos, cluster_id, vector_usuario):
    resultados = dict()
    indice = 0
    for (candidato_id, score_candidato) in candidatos.items():
        related_paper = df_ud.iloc[int(candidato_id)]
        related_paper_features = df_cl_ud.iloc[int(candidato_id)]
        c_id_candidato = related_paper_features['Label']
        if (c_id_candidato == cluster_id):
            resultados[indice] = {'course_id': candidato_id, 'title': related_paper['title'], 'url': related_paper['url']}
            indice = indice + 1

    candidatos_filtrados = []
    for (candidato_id, score_candidato) in candidatos.items():
        # related_paper = df_ud.iloc[int(candidato_id)]
        related_paper_features = df_cl_ud.iloc[int(candidato_id)]
        c_id_candidato = related_paper_features['Label']
        if (c_id_candidato != cluster_id):
            rating = related_paper_features['rating']
            if (np.isnan(rating)):
                rating = 0
            vector_candidato = [related_paper_features['difficulty'], related_paper_features['duration'], related_paper_features['n_reviews'], rating, related_paper_features['free']]
            cos_sim = dot(vector_candidato, vector_usuario)/(norm(vector_candidato)*norm(vector_usuario))
            candidatos_filtrados.append((candidato_id, cos_sim))

    candidatos_filtrados.sort(key=lambda x: x[1])
    candidatos_filtrados = candidatos_filtrados[::-1]
    c_f_indice = 0
    while(indice < 10) and (c_f_indice < len(candidatos_filtrados)):
        c_f_id = candidatos_filtrados[c_f_indice][0]
        related_paper = df_ud.iloc[int(c_f_id)]
        resultados[indice] = {'course_id': candidatos_filtrados[c_f_indice][0], 'title': related_paper['title'], 'url': related_paper['url']}
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
        related_paper = df_cou.iloc[int(candidato_id)]
        related_paper_features = df_cl_cou.iloc[int(candidato_id)]
        c_id_candidato = related_paper_features['Labels']
        if (c_id_candidato == cluster_id):
            resultados[indice] = {'course_id': candidato_id, 'title': related_paper['title'], 'url': related_paper['url']}
            indice = indice + 1
            if (indice==10):
                print("Ha llegado al limite")
                break

    candidatos_filtrados = []
    for (candidato_id, score_candidato) in candidatos.items():
        # related_paper = df_ud.iloc[int(candidato_id)]
        related_paper_features = df_cl_cou.iloc[int(candidato_id)]
        c_id_candidato = related_paper_features['Labels']
        if (c_id_candidato != cluster_id):
            rating = related_paper_features['rating']
            if (np.isnan(rating)):
                rating = 0
            vector_candidato = [related_paper_features['difficulty'], related_paper_features['total_hours'], related_paper_features['enrolled'], rating, related_paper_features['institution']]
            cos_sim = dot(vector_candidato, vector_usuario)/(norm(vector_candidato)*norm(vector_usuario))
            candidatos_filtrados.append((candidato_id, cos_sim))

    candidatos_filtrados.sort(key=lambda x: x[1])
    candidatos_filtrados = candidatos_filtrados[::-1]
    c_f_indice = 0
    while(indice < 10) and (c_f_indice < len(candidatos_filtrados)):
        c_f_id = candidatos_filtrados[c_f_indice][0]
        related_paper = df_cou.iloc[int(c_f_id)]
        resultados[indice] = {'course_id': candidatos_filtrados[c_f_indice][0], 'title': related_paper['title'], 'url': related_paper['url']}
        c_f_indice = c_f_indice + 1
        indice = indice + 1

    return resultados


@app.post("/search_courses_udacity/")
def semantic_search_udacity(query: str, contexto: Optional[ContextoUsuarioBusqueda], k: Optional[int] = 10):
    list_courses_udacity = search_courses_udacity(query, contexto.cursos_vistos, k)
    return list_courses_udacity


@app.post("/search_courses_coursera/")
def semantic_search_coursera(query: str, contexto: Optional[ContextoUsuarioBusqueda], k: Optional[int] = 10):
    list_courses_coursera = search_courses_coursera(query, contexto.cursos_vistos, k)
    return list_courses_coursera


@app.post("/recommend_udacity/")
def recommendation_udacity(perfil: PerfilUsuarioUdacity):
    query_embedding = model_udacity.encode(perfil.description, convert_to_tensor=True)

    search_hits = util.semantic_search(query_embedding, corpus_embeddings_udacity, top_k=30)
    search_hits = search_hits[0]

    results = dict()
    for hit in search_hits:
        # related_paper = df_ud.iloc[hit['corpus_id']]
        results[str(hit['corpus_id'])] = float(hit['score'])

    row_user = convertir_datos_en_features_udacity(perfil)
    df_user = pd.DataFrame([row_user], columns=["difficulty","duration","n_reviews", "rating", "free"])

    labels = clustering_model_udacity.predict(df_user)
    cluster_id = labels[0]
    list_recommendations = escoger_recomendaciones_udacity(results, cluster_id, row_user)

    return {'list_recommendations': list_recommendations}


@app.post("/recommend_coursera/")
def recommendation_coursera(perfil: PerfilUsuarioCoursera):
    query_embedding = model_coursera.encode(perfil.description, convert_to_tensor=True)

    search_hits = util.semantic_search(query_embedding, corpus_embeddings_coursera, top_k=100)
    search_hits = search_hits[0]

    results = dict()
    for hit in search_hits:
        # related_paper = df_ud.iloc[hit['corpus_id']]
        results[str(hit['corpus_id'])] = float(hit['score'])

    row_user = convertir_datos_en_features_coursera(perfil)
    df_user = pd.DataFrame([row_user], columns=["difficulty","total_hours","enrolled", "rating", "institution"])

    labels, _ = hdbscan.approximate_predict(clustering_model_coursera, df_user)
    cluster_id = labels[0]
    list_recommendations = escoger_recomendaciones_coursera(results, cluster_id, row_user)

    return {'list_recommendations': list_recommendations}


ss, mms = importar_encoders_udacity()
coursera_inst_imputer, coursera_rating_transformer, coursera_inst_encoder, coursera_powertransformer = importar_encoders_coursera()