from enum import Enum


class TechTagKind(str, Enum):
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    TOOL = "tool"


__all__ = [
    "TechTagKind",
]

