from typing import List

from pydantic import BaseModel


class PerfilUsuarioUdacity(BaseModel):
    description: str
    difficulty: str
    duration: int
    free: int
    n_reviews: int
    rating: int

class PerfilUsuarioCoursera(BaseModel):
    description: str
    difficulty: str
    duration: int
    n_reviews: int
    rating: int
    institution: str


class ContextoUsuarioBusqueda(BaseModel):
    cursos_vistos: List[int] = []