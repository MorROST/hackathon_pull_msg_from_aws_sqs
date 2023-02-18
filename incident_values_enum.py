from enum import Enum


class Incident_status(Enum):
    NEW = 1
    IN_PROCESS = 2
    CLOSE = 3
    FALSE_POSITIVE = 4
    ESCALATED = 5


class Severity(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class Incident_type(Enum):
    INCIDENTS = 1
    DISCOVERY = 2


class Action_type(Enum):
    STATUS = 1
    SEVERITY = 2
    ASSIGN_TO = 3
    ADD_COMMENT = 4
    TAG = 5
    RELEASE = 6
    FALSE_POSITIVE = 7
