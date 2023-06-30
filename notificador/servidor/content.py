from dataclasses import dataclass
from topic import *


@dataclass(frozen=True, kw_only=True, slots=True)
class Content:
    author: int
    topic: Topic
    data: str
