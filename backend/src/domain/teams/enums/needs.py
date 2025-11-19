from enum import Enum


class NeedRequirementType(str, Enum):
    MUST = "must"
    NICE = "nice"
