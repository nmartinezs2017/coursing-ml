from typing import List
from pydantic import BaseModel

class ContextoUsuario(BaseModel):
    cursos_descartados: List[int] = []


class PerfilUsuario(BaseModel):
    description: str
    difficulty: str = 'beginner'
    duration: int = 10
    free: int = 1
    n_reviews: int = 100
    rating: float = 4.7
    institution: str = ""