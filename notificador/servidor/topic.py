from typing import List

class Topic():
    def __init__(self,id,name):
        self.id: int  = id#ID único
        self.name: str = name#Nome do tópico
        self.list_subscribers: List[str] = []
