from typing import List
from pydantic import BaseModel

class ContextoUsuario(BaseModel):
    cursos_descartados: List[int] = []
    lista_idiomas: List[str] = []

class PerfilUsuario(BaseModel):
    description: str = " "
    difficulty: str = 'beginner'
    duration: int = 20
    free: int = 1
    n_reviews: int = 20000
    rating: float = 4.5
    institution: str = "Coursera"
    cost: float = 10