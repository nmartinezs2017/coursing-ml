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

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/search_courses_udacity/")
def semantic_search_udacity(query: str, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    list_courses_udacity = search_courses_udacity(query, contexto.cursos_descartados, k)
    return list_courses_udacity


@app.post("/search_courses_coursera/")
def semantic_search_coursera(query: str, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    list_courses_coursera = search_courses_coursera(query, contexto.cursos_descartados, k)
    return list_courses_coursera


@app.post("/recommend_udacity/")
def recommendation_udacity(perfil: PerfilUsuario):
    list_recommendations = crear_lista_recomendaciones_udacity(perfil)
    return {'list_recommendations': list_recommendations}


@app.post("/recommend_coursera/")
def recommendation_coursera(perfil: PerfilUsuario):
    list_recommendations = crear_lista_recomendaciones_coursera(perfil)
    return {'list_recommendations': list_recommendations}


@app.post("/explore/")
def explore_courses(perfil: PerfilUsuario, contexto: Optional[ContextoUsuario], k: Optional[int] = 10):
    list_courses_udacity = explore_courses_udacity(perfil, contexto, k)
    list_courses_coursera = explore_courses_coursera(perfil, contexto, k)
    return {"courses_udacity": list_courses_udacity, "courses_coursera": list_courses_coursera}
