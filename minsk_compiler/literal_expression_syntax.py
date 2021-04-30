from minsk_compiler.expression_syntax import ExpressionSyntax
from minsk_compiler.syntax_kind import SyntaxKind
from minsk_compiler.syntax_token import SyntaxToken
from typing import Iterable
from minsk_compiler.syntax_node import SyntaxNode


class LiteralExpressionSyntax(ExpressionSyntax):
    literal_token: SyntaxToken

    def __init__(self, literal_token: SyntaxToken):
        self.literal_token = literal_token

    def kind(self) -> SyntaxKind:
        return SyntaxKind.LITERAL_EXPRESSION

    def children(self) -> Iterable["SyntaxNode"]:
        return (self.literal_token, )
