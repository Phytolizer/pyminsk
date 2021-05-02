from typing import Optional, Iterable

from minsk.code_analysis.syntax.syntax_kind import SyntaxKind


def get_binary_operator_precedence(kind: SyntaxKind) -> int:
    if kind in (SyntaxKind.STAR_TOKEN, SyntaxKind.SLASH_TOKEN):
        return 5
    elif kind in (SyntaxKind.PLUS_TOKEN, SyntaxKind.MINUS_TOKEN):
        return 4
    elif kind in (SyntaxKind.EQUALS_EQUALS_TOKEN, SyntaxKind.BANG_EQUALS_TOKEN):
        return 3
    elif kind == SyntaxKind.AMPERSAND_AMPERSAND_TOKEN:
        return 2
    elif kind == SyntaxKind.PIPE_PIPE_TOKEN:
        return 1
    else:
        return 0


def get_unary_operator_precedence(kind: SyntaxKind) -> int:
    if kind in (SyntaxKind.PLUS_TOKEN, SyntaxKind.MINUS_TOKEN, SyntaxKind.BANG_TOKEN):
        return 6
    else:
        return 0


def keyword_kind(text: str) -> SyntaxKind:
    if text == "true":
        return SyntaxKind.TRUE_KEYWORD
    elif text == "false":
        return SyntaxKind.FALSE_KEYWORD
    else:
        return SyntaxKind.IDENTIFIER_TOKEN


def text_for(kind: SyntaxKind) -> Optional[str]:
    if kind == SyntaxKind.PLUS_TOKEN:
        return "+"
    elif kind == SyntaxKind.MINUS_TOKEN:
        return "-"
    elif kind == SyntaxKind.STAR_TOKEN:
        return "*"
    elif kind == SyntaxKind.SLASH_TOKEN:
        return "/"
    elif kind == SyntaxKind.BANG_TOKEN:
        return "!"
    elif kind == SyntaxKind.EQUALS_TOKEN:
        return "="
    elif kind == SyntaxKind.AMPERSAND_AMPERSAND_TOKEN:
        return "&&"
    elif kind == SyntaxKind.PIPE_PIPE_TOKEN:
        return "||"
    elif kind == SyntaxKind.EQUALS_EQUALS_TOKEN:
        return "=="
    elif kind == SyntaxKind.BANG_EQUALS_TOKEN:
        return "!="
    elif kind == SyntaxKind.OPEN_PARENTHESIS_TOKEN:
        return "("
    elif kind == SyntaxKind.CLOSE_PARENTHESIS_TOKEN:
        return ")"
    elif kind == SyntaxKind.FALSE_KEYWORD:
        return "false"
    elif kind == SyntaxKind.TRUE_KEYWORD:
        return "true"
    return None


def binary_operators() -> Iterable[SyntaxKind]:
    return filter(lambda k: get_binary_operator_precedence(k) != 0, SyntaxKind)
