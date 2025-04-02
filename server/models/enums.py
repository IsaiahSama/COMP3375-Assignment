from enum import Enum


class Roles(Enum):
    USER = "user"
    ADMIN = "admin"

class Status(Enum):
    REPORTED = "reported"
    PENDING = "pending"
    APPROVED = "approved"
    IN_PROGRESS = "in progress"
    REJECTED = "rejected"

class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
