import os
import sys
from fastapi import FastAPI
from typing import Optional, List
csfp = os.path.abspath(os.path.dirname(__file__))
if csfp not in sys.path:
    sys.path.insert(0, csfp)
from search import *
from explore import *
from models import *
from recommendation import *

app = FastAPI()


@app.post("/search_courses_udacity/")
def semantic_search_udacity(query: str, contexto: Optional[UserContext], k: Optional[int] = 10):
    list_courses_udacity = search_courses_udacity(query, contexto, k)
    return list_courses_udacity


@app.post("/search_courses_coursera/")
def semantic_search_coursera(query: str, contexto: Optional[UserContext], k: Optional[int] = 10):
    list_courses_coursera = search_courses_coursera(query, contexto, k)
    return list_courses_coursera


@app.post("/search_courses_udemy/")
def semantic_search_udemy(query: str, contexto: Optional[UserContext], k: Optional[int] = 10):
    list_courses_udemy = search_courses_udemy(query, contexto, k)
    return list_courses_udemy


@app.post("/search_courses_global/")
def semantic_search_global(query: str, contexto: Optional[UserContext], k: Optional[int] = 10):
    list_courses_udacity = search_courses_udacity(query, contexto, k)
    list_courses_coursera = search_courses_coursera(query, contexto, k)
    list_courses_udemy = search_courses_udemy(query, contexto, k)
    return {"courses_udacity": list_courses_udacity, "courses_coursera": list_courses_coursera, "courses_udemy": list_courses_udemy}


@app.post("/recommend_courses_udacity/")
def recommendation_udacity(perfil: UserProfile, contexto: Optional[UserContext], k: Optional[int] = 10):
    list_recommendations = create_list_recommendations_udacity(perfil, contexto, k)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_courses_udemy/")
def recommendation_udemy(perfil: UserProfile, contexto: Optional[UserContext], k: Optional[int] = 10):
    list_recommendations = create_list_recommendations_udemy(perfil, contexto, k)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_courses_coursera/")
def recommendation_coursera(perfil: UserProfile, contexto: Optional[UserContext], k: Optional[int] = 10):
    list_recommendations = create_list_recommendations_coursera(perfil, contexto, k)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_courses_global/")
def recommendation_global(perfil: UserProfile, contexto: Optional[UserContext], k: Optional[int] = 10):
    list_courses_coursera = create_list_recommendations_coursera(perfil, contexto, k)
    list_courses_udemy = create_list_recommendations_udemy(perfil, contexto, k)
    list_courses_udacity = create_list_recommendations_udacity(perfil, contexto, k)
    return {"courses_udacity": list_courses_udacity, "courses_coursera": list_courses_coursera, "courses_udemy": list_courses_udemy}


@app.post("/recommend_related_courses_udacity/")
def recommendation_udacity(perfil: UserProfile, id_course: int, contexto: Optional[UserContext], k: Optional[int] = 10):
    curso_description = get_curso_udacity(id_course)["description"]
    list_recommendations = create_list_recommendations_udacity(perfil, contexto, k, curso_description)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_related_courses_coursera/")
def recommendation_coursera(perfil: UserProfile, id_course: int, contexto: Optional[UserContext], k: Optional[int] = 10):
    curso_description = get_curso_coursera(id_course)["description"]
    list_recommendations = create_list_recommendations_coursera(perfil, contexto, k, curso_description)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_related_courses_udemy/")
def recommendation_udemy(perfil: UserProfile, id_course: int, contexto: Optional[UserContext], k: Optional[int] = 10):
    curso_description = get_curso_udemy(id_course)["description"]
    curso_description_extend = get_curso_udemy(id_course)["description"]
    curso_description = curso_description + curso_description_extend
    list_recommendations = create_list_recommendations_udemy(perfil, contexto, k, curso_description)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_related_query_udacity/")
def recommendation_udacity(perfil: UserProfile, query:str, contexto: Optional[UserContext], k: Optional[int] = 10):
    list_recommendations = create_list_recommendations_udacity(perfil, contexto, k, query)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_related_query_coursera/")
def recommendation_coursera(perfil: UserProfile, query:str, contexto: Optional[UserContext], k: Optional[int] = 10):
    list_recommendations = create_list_recommendations_coursera(perfil, contexto, k, query)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_related_query_udemy/")
def recommendation_udemy(perfil: UserProfile, query:str, contexto: Optional[UserContext], k: Optional[int] = 10):
    list_recommendations = create_list_recommendations_udemy(perfil, contexto, k, query)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_related_query_global/")
def recommendation_udemy(perfil: UserProfile, query:str, contexto: Optional[UserContext], k: Optional[int] = 10):
    list_courses_coursera = create_list_recommendations_coursera(perfil, contexto, k, query)
    list_courses_udemy = create_list_recommendations_udemy(perfil, contexto, k, query)
    list_courses_udacity = create_list_recommendations_udacity(perfil, contexto, k, query)
    return {"courses_udacity": list_courses_udacity, "courses_coursera": list_courses_coursera, "courses_udemy": list_courses_udemy}


@app.post("/explore/")
def explore_courses(perfil: UserProfile, contexto: Optional[UserContext], k: Optional[int] = 10):
    print("Hola")
    list_courses_udacity = explore_courses_udacity(perfil, contexto, k)
    print("A")
    list_courses_coursera = explore_courses_coursera(perfil, contexto, k)
    print("B")
    list_courses_udemy = explore_courses_udemy(perfil, contexto, k)
    print("C")
    return {"courses_udacity": list_courses_udacity, "courses_coursera": list_courses_coursera, "courses_udemy": list_courses_udemy}
