from dataclasses import dataclass
from fila import Fila
from typing import Callable, Optional, Tuple, TypeAlias
from content import Content

FnNotify: TypeAlias = Callable[[list[Content]], None]

@dataclass(frozen=True, kw_only=True, slots=True)
class UserInfo:
    user_id: str
    online: bool = False
    fila: Fila = Fila()
    callback: FnNotify