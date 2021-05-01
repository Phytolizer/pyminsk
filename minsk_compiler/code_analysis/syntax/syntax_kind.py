from enum import Enum, auto

from stringcase import pascalcase, lowercase


class SyntaxKind(Enum):
    # Special tokens
    END_OF_FILE_TOKEN = auto()
    BAD_TOKEN = auto()

    # Regular tokens
    IDENTIFIER_TOKEN = auto()
    NUMBER_TOKEN = auto()
    WHITESPACE_TOKEN = auto()
    PLUS_TOKEN = auto()
    MINUS_TOKEN = auto()
    STAR_TOKEN = auto()
    SLASH_TOKEN = auto()
    OPEN_PARENTHESIS_TOKEN = auto()
    CLOSE_PARENTHESIS_TOKEN = auto()
    BANG_TOKEN = auto()
    AMPERSAND_AMPERSAND_TOKEN = auto()
    PIPE_PIPE_TOKEN = auto()
    EQUALS_EQUALS_TOKEN = auto()
    BANG_EQUALS_TOKEN = auto()

    # Keywords
    TRUE_KEYWORD = auto()
    FALSE_KEYWORD = auto()

    # Expression nodes
    LITERAL_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()
    PARENTHESIZED_EXPRESSION = auto()

    def __str__(self) -> str:
        return pascalcase(lowercase(self.name))
