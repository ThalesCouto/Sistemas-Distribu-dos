from dataclasses import dataclass
from fila import Fila

@dataclass(frozen=True, kw_only=True, slots=True)
class UserInfo:
    user_id: int
    user_name: str
    fila: Fila = Fila()