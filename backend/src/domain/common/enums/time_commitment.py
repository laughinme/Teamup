from enum import Enum


class TimeCommitment(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


__all__ = [
    "TimeCommitment",
]

