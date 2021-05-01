from enum import Enum, auto
from stringcase import pascalcase, lowercase


class SyntaxKind(Enum):
    END_OF_FILE_TOKEN = auto()
    BAD_TOKEN = auto()
    NUMBER_TOKEN = auto()
    WHITESPACE_TOKEN = auto()
    PLUS_TOKEN = auto()
    MINUS_TOKEN = auto()
    STAR_TOKEN = auto()
    SLASH_TOKEN = auto()
    OPEN_PARENTHESIS_TOKEN = auto()
    CLOSE_PARENTHESIS_TOKEN = auto()

    LITERAL_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()
    PARENTHESIZED_EXPRESSION = auto()

    def __str__(self) -> str:
        return pascalcase(lowercase(self.name))
