from enum import Enum


class Direction(str, Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    MOBILE = "mobile"
    MLOPS = "mlops"


__all__ = [
    "Direction",
]

