from enum import Enum, auto


class BoundNodeKind(Enum):
    UNARY_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()
    LITERAL_EXPRESSION = auto()
    VARIABLE_EXPRESSION = auto()
    ASSIGNMENT_EXPRESSION = auto()
