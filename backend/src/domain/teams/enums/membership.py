from enum import Enum


class TeamMembershipOrigin(str, Enum):
    INVITE = "invite"
    APPLICATION = "application"
    SYSTEM = "system"


class TeamInviteStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class TeamApplicationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class TeamMemberStatus(str, Enum):
    INVITED = "invited"
    APPLIED = "applied"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    LEFT = "left"


__all__ = [
    "TeamMembershipOrigin",
    "TeamInviteStatus",
    "TeamApplicationStatus",
    "TeamMemberStatus",
]
