from dataclasses import dataclass
from fila import Fila

@dataclass
class Topic():
    id: int #ID único
    name: str #Nome do tópico
    list_subscribers: list = [] #Lista de inscritos no tópico
    fila: Fila = Fila()