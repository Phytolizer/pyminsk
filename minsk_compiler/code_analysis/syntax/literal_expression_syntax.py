from typing import Sequence, Any

from minsk_compiler.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk_compiler.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk_compiler.code_analysis.syntax.syntax_node import SyntaxNode
from minsk_compiler.code_analysis.syntax.syntax_token import SyntaxToken


class LiteralExpressionSyntax(ExpressionSyntax):
    literal_token: SyntaxToken

    def __init__(self, literal_token: SyntaxToken, value: Any = None):
        if value is None:
            value = literal_token.value
        self.literal_token = literal_token
        self.value = value

    def kind(self) -> SyntaxKind:
        return SyntaxKind.LITERAL_EXPRESSION

    def children(self) -> Sequence["SyntaxNode"]:
        return self.literal_token,
