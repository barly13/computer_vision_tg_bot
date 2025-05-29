from dataclasses import dataclass
from typing import Any


@dataclass
class Response:
    value: Any = None
    message: str = None
    error: bool = False
