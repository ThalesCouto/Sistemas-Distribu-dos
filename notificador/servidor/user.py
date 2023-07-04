from dataclasses import dataclass
from fila import Fila
from typing import Callable, Optional, Tuple, TypeAlias
from content import Content

FnNotify: TypeAlias = Callable[[list[Content]], None]

class UserInfo:
    def __init__(self,id: str,callback: FnNotify) -> None:
        self.user_id: str = id
        self.callback: FnNotify = callback
        self.online: bool = False
        self.fila: Fila = Fila()
