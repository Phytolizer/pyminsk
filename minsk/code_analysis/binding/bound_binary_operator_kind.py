from enum import Enum, auto


class BoundBinaryOperatorKind(Enum):
    ADDITION = auto()
    SUBTRACTION = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()
    LOGICAL_AND = auto()
    LOGICAL_OR = auto()

    EQUALITY = auto()
    INEQUALITY = auto()
