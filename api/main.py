from fastapi import FastAPI
from typing import Optional
import pandas as pd
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
from kedro.framework.context.context import load_context
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing

app = FastAPI()

context = load_context('../coursing-ml/')

model_udacity = context.catalog.load("nlp_model_udacity")
model_coursera = context.catalog.load("nlp_model_coursera")
clustering_model_udacity = context.catalog.load("clustering_model_udacity")
df_ud = context.catalog.load("preprocessed_udacity")
corpus_embeddings_udacity = context.catalog.load("corpus_embeddings_udacity")
df_cl_ud = context.catalog.load("clustering_output_udacity")

## Encoders
ss = StandardScaler()
mms = MinMaxScaler()
enc = preprocessing.OrdinalEncoder()

class PerfilUsuario(BaseModel):
    description: str
    difficulty: int
    duration: int
    free: bool
    rating: int

def inicializar_encoders():
    ss.fit(df_ud[['duration']])
    mms.fit(df_ud[['rating']])
    enc.fit(df_ud[['difficulty']])

def convertir_datos_en_features(perfil: PerfilUsuario):
    user_difficulty = enc.transform(perfil.difficulty)
    user_duration = ss.transform(perfil.duration)
    user_free = 1 if perfil.free else 0
    rating = mms.transform(perfil.rating)


def recommendation(perfil: PerfilUsuario):
    query_embedding = model_udacity.encode(perfil.description, convert_to_tensor=True)

    search_hits = util.semantic_search(query_embedding, corpus_embeddings_udacity)
    search_hits = search_hits[0]  #Get the hits for the first query

    results = dict()
    for hit in search_hits:
        results[str(hit['corpus_id'])] = float(hit['score'])

    row_user = convertir_datos_en_features(perfil)

    df_user = pd.DataFrame([[a, b, c]], columns=['a', 'b', 'c'])
    labels = clustering_model_udacity.predict(df_user)

    return results

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
        # print("{:.2f}\t{}".format(hit['score'], related_paper))

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