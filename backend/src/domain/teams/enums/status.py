from enum import Enum


class TeamStatus(str, Enum):
    DRAFT = "draft"
    RECRUITING = "recruiting"
    FULL = "full"
    CLOSED = "closed"
