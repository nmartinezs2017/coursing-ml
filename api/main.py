from fastapi import FastAPI
from typing import Optional
import pandas as pd
import numpy as np
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
from kedro.framework.context.context import load_context
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from numpy import dot
from numpy.linalg import norm

app = FastAPI()

context = load_context('../coursing-ml/')

model_udacity = context.catalog.load("nlp_model_udacity")
model_coursera = context.catalog.load("nlp_model_coursera")
clustering_model_udacity = context.catalog.load("clustering_model_udacity")
df_ud = context.catalog.load("fe_udacity")
X_train = context.catalog.load("preprocessed_udacity")
corpus_embeddings_udacity = context.catalog.load("corpus_embeddings_udacity")
df_cl_ud = context.catalog.load("clustering_output_udacity")

## Encoders
ss = StandardScaler()
mms = MinMaxScaler()

class PerfilUsuario(BaseModel):
    description: str
    difficulty: str
    duration: int
    free: int
    n_reviews: int
    rating: int

def inicializar_encoders():
    X_train[['duration']].fillna("", inplace=True)
    X_train[['rating']].fillna("", inplace=True)
    ss.fit(X_train[['duration']])
    mms.fit(X_train[['rating']])

def convertir_datos_en_features(perfil: PerfilUsuario):
    user_difficulty = 1
    if (perfil.difficulty == 'beginner'):
        user_difficulty = 1
    elif (perfil.difficulty == 'intermediate'):
        user_difficulty = 2
    else:
        user_difficulty = 0
    user_duration = ss.transform([[perfil.duration]])
    user_free = perfil.free
    user_popularity = 0
    user_rating = mms.transform([[perfil.rating]])

    return [user_difficulty, user_duration[0][0], user_free, user_popularity, user_rating[0][0],1, 1, 1, 1, 1, 1, 1]

def escoger_recomendaciones(candidatos, cluster_id, vector_usuario):
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
        related_paper = df_ud.iloc[int(candidato_id)]
        related_paper_features = df_cl_ud.iloc[int(candidato_id)]
        c_id_candidato = related_paper_features['Label']
        if (c_id_candidato != cluster_id):
            rating = related_paper['rating']
            if (np.isnan(rating)):
                rating = 0
            vector_candidato = [related_paper['difficulty'], related_paper['duration'], related_paper['free'], related_paper['n_reviews'], rating, related_paper['school_Career Advancement'], related_paper['school_School of Artificial Intelligence'], related_paper['school_School of Autonomous Systems'], related_paper['school_School of Business'], related_paper['school_School of Cloud Computing'], related_paper['school_School of Data Science'], related_paper['school_School of Programming & Development']]
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

def search_courses_udacity(title, description = ""):
    query_embedding = model_udacity.encode(title+' '+description, convert_to_tensor=True)

    search_hits = util.semantic_search(query_embedding, corpus_embeddings_udacity)
    search_hits = search_hits[0]  #Get the hits for the first query

    results = dict()
    print("\n\nCourse:", title)
    print("Most similar course:")
    for hit in search_hits:
        related_paper = df_ud.iloc[hit['corpus_id']]
        results[str(hit['corpus_id'])] = float(hit['score'])
        print("{:.2f}\t{}".format(hit['score'], related_paper['title']))

    return dict(results)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/search_courses/")
def semantic_search(title: str, description: Optional[str] = ""):
    list_courses_udacity = search_courses_udacity(title, description)
    return list_courses_udacity

@app.get("/clustering/course-cluster/{id_course}")
def get_course_cluster(id_course: int):
    return {'id_course': id_course, 'clustering_id': df_cl_ud.iloc[id_course]['Label']}

@app.get("/clustering/courses-list/{id_cluster}")
def get_list_cluster(id_cluster: int):
    list_courses = df_cl_ud[df_cl_ud['Label']==id_cluster].index.tolist()
    return {'clustering_id': id_cluster, 'list_courses': list_courses}

@app.get("/clustering/clusters-list/")
def get_list_cluster():
    list_courses = df_cl_ud['Label'].unique().tolist()
    return {'list_courses': list_courses}


@app.post("/recommend/")
def recommendation(perfil: PerfilUsuario):
    query_embedding = model_udacity.encode(perfil.description, convert_to_tensor=True)

    search_hits = util.semantic_search(query_embedding, corpus_embeddings_udacity, top_k=30)
    search_hits = search_hits[0]

    results = dict()
    for hit in search_hits:
        # related_paper = df_ud.iloc[hit['corpus_id']]
        results[str(hit['corpus_id'])] = float(hit['score'])

    row_user = convertir_datos_en_features(perfil)
    df_user = pd.DataFrame([row_user], columns=["difficulty","duration","free","n_reviews","rating","school_Career Advancement","school_School of Artificial Intelligence","school_School of Autonomous Systems","school_School of Business","school_School of Cloud Computing","school_School of Data Science","school_School of Programming & Development"])

    labels = clustering_model_udacity.predict(df_user)
    cluster_id = labels[0]
    list_recommendations = escoger_recomendaciones(results, cluster_id, row_user)

    return {'list_recommendations': list_recommendations}


inicializar_encoders()