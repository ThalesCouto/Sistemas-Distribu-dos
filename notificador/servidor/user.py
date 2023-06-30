from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True, slots=True)
class UserInfo:
    user_id: int
    user_name: str