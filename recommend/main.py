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
def semantic_search_udacity(query: str, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    list_courses_udacity = search_courses_udacity(query, contexto.cursos_descartados, k)
    return list_courses_udacity


@app.post("/search_courses_coursera/")
def semantic_search_coursera(query: str, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    list_courses_coursera = search_courses_coursera(query, contexto.cursos_descartados, k)
    return list_courses_coursera


@app.post("/search_courses_udemy/")
def semantic_search_udemy(query: str, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    list_courses_udemy = search_courses_udemy(query, contexto.cursos_descartados, k)
    return list_courses_udemy


@app.post("/recommend_courses_udacity/")
def recommendation_udacity(perfil: PerfilUsuario, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    list_recommendations = crear_lista_recomendaciones_udacity(perfil, contexto, k)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_courses_udemy/")
def recommendation_coursera(perfil: PerfilUsuario, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    list_recommendations = crear_lista_recomendaciones_udemy(perfil, contexto, k)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_courses_coursera/")
def recommendation_coursera(perfil: PerfilUsuario, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    list_recommendations = crear_lista_recomendaciones_coursera(perfil, contexto, k)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_related_courses_udacity/")
def recommendation_udacity(perfil: PerfilUsuario, id_course: int, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    curso_description = get_curso_udacity(id_course)["description"]
    list_recommendations = crear_lista_recomendaciones_udacity(perfil, contexto, k, curso_description)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_related_courses_coursera/")
def recommendation_coursera(perfil: PerfilUsuario, id_course: int, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    curso_description = get_curso_coursera(id_course)["description"]
    list_recommendations = crear_lista_recomendaciones_coursera(perfil, contexto, k, curso_description)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_related_courses_udemy/")
def recommendation_udemy(perfil: PerfilUsuario, id_course: int, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    curso_description = get_curso_udemy(id_course)["description"]
    curso_description_extend = get_curso_udemy(id_course)["description"]
    curso_description = curso_description + curso_description_extend
    list_recommendations = crear_lista_recomendaciones_udemy(perfil, contexto, k, curso_description)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_related_query_udacity/")
def recommendation_udacity(perfil: PerfilUsuario, query:str, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    list_recommendations = crear_lista_recomendaciones_udacity(perfil, contexto, k, query)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_related_query_coursera/")
def recommendation_coursera(perfil: PerfilUsuario, query:str, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    list_recommendations = crear_lista_recomendaciones_coursera(perfil, contexto, k, query)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_related_query_udemy/")
def recommendation_udemy(perfil: PerfilUsuario, query:str, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    list_recommendations = crear_lista_recomendaciones_udemy(perfil, contexto, k, query)
    return {'list_recommendations': list_recommendations}


@app.post("/explore/")
def explore_courses(perfil: PerfilUsuario, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    list_courses_udacity = explore_courses_udacity(perfil, contexto, k)
    list_courses_coursera = explore_courses_coursera(perfil, contexto, k)
    list_courses_udemy = explore_courses_udemy(perfil, contexto, k)
    return {"courses_udacity": list_courses_udacity, "courses_coursera": list_courses_coursera, "courses_udemy": list_courses_udemy}
