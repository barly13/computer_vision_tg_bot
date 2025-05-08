from dataclasses import dataclass


@dataclass
class Response:
    value = None
    message: str = None
    error: bool = False
