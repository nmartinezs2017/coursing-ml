import os
import pickle
import sys
import numpy as np
from numpy import dot
from numpy.linalg import norm
import hdbscan
import pandas as pd
csfp = os.path.abspath(os.path.dirname(__file__))
if csfp not in sys.path:
    sys.path.insert(0, csfp)
from models import *
from sentence_transformers import util

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

def filter_courses(cursos_candidatos, contexto, proveedor):
    resultado = []
    for candidato_id, score in cursos_candidatos:
        if proveedor == "coursera":
            curso_candidato = get_curso_coursera(candidato_id)
        elif proveedor == "udemy":
            curso_candidato = get_curso_udemy(candidato_id)
        else:
            curso_candidato = get_curso_udacity(candidato_id)
        idioma_correcto = curso_candidato.language in contexto.language_list
        nuevo_contenido = candidato_id not in contexto.discarded_courses
        if idioma_correcto and nuevo_contenido:
            resultado.append((candidato_id, score))
    return resultado


def compute_distance_udacity(usuario_embedding, curso_id):
    curso = df_cl_ud.iloc[curso_id]
    rating = curso['rating']
    if (np.isnan(rating)):
        rating = 0
    curso_embedding = [curso['difficulty'], curso['duration'], curso['n_reviews'], rating, curso['free']]
    cos_sim = dot(curso_embedding, usuario_embedding) / (norm(curso_embedding) * norm(usuario_embedding))
    return cos_sim


def compute_distance_coursera(usuario_embedding, curso_id):
    curso = df_cl_cou.iloc[curso_id]
    rating = curso['rating']
    if (np.isnan(rating)):
        rating = 0
    curso_embedding = [curso['difficulty'], curso['total_hours'], curso['enrolled'], rating, curso['institution']]
    cos_sim = dot(curso_embedding, usuario_embedding) / (norm(curso_embedding) * norm(usuario_embedding))
    return cos_sim


def compute_distance_udemy(usuario_embedding, curso_id):
    curso = df_cl_ude.iloc[curso_id]
    curso_embedding = [curso['cost'], curso['n_students'], curso['rating'], curso['hours']]
    cos_sim = dot(curso_embedding, usuario_embedding) / (norm(curso_embedding) * norm(usuario_embedding))
    return cos_sim


def content_similarity_udacity(perfil_description, curso_description):
    if pd.isna(curso_description):
        curso_description = ""
    if pd.isna(perfil_description):
        perfil_description = ""
    usuario_embedding = model_udacity.encode(perfil_description, convert_to_tensor=True)
    curso_embedding = model_udacity.encode(curso_description, convert_to_tensor=True)
    cos_score = util.pytorch_cos_sim(usuario_embedding, curso_embedding)[0]
    return cos_score


def content_similarity_coursera(perfil_description, curso_description):
    if pd.isna(curso_description):
        curso_description = ""
    if pd.isna(perfil_description):
        perfil_description = ""
    usuario_embedding = model_coursera.encode(perfil_description, convert_to_tensor=True)
    curso_embedding = model_coursera.encode(curso_description, convert_to_tensor=True)
    cos_score = util.pytorch_cos_sim(usuario_embedding, curso_embedding)[0]
    return cos_score


def content_similarity_udemy(perfil_description, curso_description):
    if pd.isna(curso_description):
        curso_description = ""
    if pd.isna(perfil_description):
        perfil_description = ""
    usuario_embedding = model_udemy.encode(perfil_description, convert_to_tensor=True)
    curso_embedding = model_udemy.encode(curso_description, convert_to_tensor=True)
    cos_score = util.pytorch_cos_sim(usuario_embedding, curso_embedding)[0]
    return cos_score


def get_curso_udacity(id: int):
    return df_ud.iloc[id]


def get_curso_coursera(id: int):
    return df_cou.iloc[id]


def get_curso_udemy(id: int):
    return df_ude.iloc[id]


def import_encoders_udacity():
    pkl_file = open('encoders/encoders_udacity.pkl', 'rb')
    encoders_dict = pickle.load(pkl_file)
    pkl_file.close()
    ss = encoders_dict["udacity_duration_ss"]
    mms = encoders_dict["udacity_rating_mms"]
    return ss, mms


def import_encoders_udemy():
    pkl_file = open('encoders/encoders_udemy.pkl', 'rb')
    udemy_encoders_dict = pickle.load(pkl_file)
    pkl_file.close()
    udemy_powertransformer = udemy_encoders_dict["udemy_powertransformer"]
    return udemy_powertransformer


def import_encoders_coursera():
    pkl_file = open('encoders/encoders_coursera.pkl', 'rb')
    coursera_encoders_dict = pickle.load(pkl_file)
    coursera_inst_imputer = coursera_encoders_dict["coursera_inst_imputer"]
    coursera_rating_transformer = coursera_encoders_dict["coursera_rating_transformer"]
    coursera_inst_encoder = coursera_encoders_dict["coursera_inst_encoder"]
    coursera_powertransformer = coursera_encoders_dict["coursera_powertransformer"]
    pkl_file.close()
    return coursera_inst_imputer, coursera_rating_transformer, coursera_inst_encoder, coursera_powertransformer


def convertir_datos_en_features_coursera(perfil: UserProfile):
    if (perfil.difficulty == 'beginner'):
        user_difficulty = 0
    elif (perfil.difficulty == 'intermediate'):
        user_difficulty = 1
    else:
        user_difficulty = 2
    df_user = pd.DataFrame([[user_difficulty, perfil.duration, perfil.students, perfil.rating, 0.1807892321810951]], columns=["difficulty","total_hours","enrolled", "rating", "institution"])
    df_user['rating'] = coursera_rating_transformer.transform(df_user[['rating']])
    numerical_features = ['difficulty', 'total_hours', 'enrolled', 'rating']
    df_user[numerical_features] = coursera_powertransformer.transform(df_user[numerical_features])
    # df_user = coursera_inst_encoder.transform(df_user)
    return df_user.iloc[0].to_numpy()


def convertir_datos_en_features_udacity(perfil: UserProfile):
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


def convertir_datos_en_features_udemy(perfil: UserProfile):
    df_user = pd.DataFrame([[perfil.cost, perfil.students, perfil.rating, perfil.duration]], columns=['cost', 'n_students', 'rating', 'hours'])
    numerical_features = ['cost', 'n_students', 'rating', 'hours']
    df_user[numerical_features] = coursera_powertransformer.transform(df_user[numerical_features])

    return df_user.iloc[0].to_numpy()


def predecir_cluster_udacity(feature_usuario):
    df_user = pd.DataFrame([feature_usuario], columns=["difficulty","duration","n_reviews", "rating", "free"])
    labels = clustering_model_udacity.predict(df_user)
    return labels[0]


def predecir_cluster_coursera(feature_usuario):
    df_user = pd.DataFrame([feature_usuario], columns=["difficulty","total_hours","enrolled", "rating", "institution"])
    labels, _ = hdbscan.approximate_predict(clustering_model_coursera, df_user)
    return labels[0]


def predecir_cluster_udemy(feature_usuario):
    df_user = pd.DataFrame([feature_usuario], columns=['cost', 'n_students', 'rating', 'hours'])
    labels, _ = hdbscan.approximate_predict(clustering_model_udemy, df_user)
    return labels[0]


##### inicialización #####
ss, mms = import_encoders_udacity()
coursera_inst_imputer, coursera_rating_transformer, coursera_inst_encoder, coursera_powertransformer = import_encoders_coursera()
udemy_powertransformer = import_encoders_udemy()