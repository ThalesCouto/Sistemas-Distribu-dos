from dataclasses import dataclass
import sys
from typing import TYPE_CHECKING

IS_NEW_PYTHON: bool = sys.version_info >= (3, 8)
if IS_NEW_PYTHON:
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias
    
if IS_NEW_PYTHON:
    @dataclass
    class Content:
        author: str
        topic: str
        data: str
elif not TYPE_CHECKING:
    @dataclass
    class Content:
        author: str
        topic: str
        data: str