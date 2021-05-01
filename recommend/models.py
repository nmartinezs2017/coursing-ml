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


class ContextoUsuario(BaseModel):
    cursos_vistos: List[int] = []


class PerfilUsuarioExplorar(BaseModel):
    description: str
    difficulty: str = 'beginner'
    duration: int = 10
    free: int = 1
    n_reviews: int = 100
    rating: float = 4.7
    institution: str = ""