from enum import Enum, auto


class BoundUnaryOperatorKind(Enum):
    IDENTITY = auto()
    NEGATION = auto()
    LOGICAL_NEGATION = auto()
