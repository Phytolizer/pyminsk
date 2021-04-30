from enum import Enum, auto


class SyntaxKind(Enum):
    END_OF_FILE_TOKEN = auto()
    BAD_TOKEN = auto()
    NUMBER_TOKEN = auto()
    WHITESPACE_TOKEN = auto()
    PLUS_TOKEN = auto()
    MINUS_TOKEN = auto()
    STAR_TOKEN = auto()
    SLASH_TOKEN = auto()

    def __str__(self) -> str:
        return self.name
