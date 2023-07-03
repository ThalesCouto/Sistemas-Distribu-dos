from dataclasses import dataclass
from fila import Fila

@dataclass(frozen=True, kw_only=True, slots=True)
class UserInfo:
    user_id: str
    online: bool = False
    fila: Fila = Fila()