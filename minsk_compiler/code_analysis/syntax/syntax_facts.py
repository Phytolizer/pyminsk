from minsk_compiler.code_analysis.syntax.syntax_kind import SyntaxKind


def get_binary_operator_precedence(kind: SyntaxKind) -> int:
    if kind in (SyntaxKind.STAR_TOKEN, SyntaxKind.SLASH_TOKEN):
        return 2
    elif kind in (SyntaxKind.PLUS_TOKEN, SyntaxKind.MINUS_TOKEN):
        return 1
    else:
        return 0


def get_unary_operator_precedence(kind: SyntaxKind) -> int:
    if kind in (SyntaxKind.PLUS_TOKEN, SyntaxKind.MINUS_TOKEN):
        return 3
    else:
        return 0
