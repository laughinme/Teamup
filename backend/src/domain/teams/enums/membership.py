from enum import Enum


class TeamMembershipOrigin(str, Enum):
    INVITE = "invite"
    APPLICATION = "application"
    SYSTEM = "system"


class TeamInviteStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"
    CANCELED = "canceled"


class TeamApplicationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELED = "canceled"
