from dataclasses import dataclass
from typing import Sequence, Any

from minsk.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_node import SyntaxNode
from minsk.code_analysis.syntax.syntax_token import SyntaxToken
from minsk.code_analysis.text_span import TextSpan


@dataclass
class LiteralExpressionSyntax(ExpressionSyntax):
    literal_token: SyntaxToken
    value: Any

    def __init__(self, literal_token: SyntaxToken, value: Any = None):
        if value is None:
            value = literal_token.value
        self.literal_token = literal_token
        self.value = value

    def kind(self) -> SyntaxKind:
        return SyntaxKind.LITERAL_EXPRESSION

    def children(self) -> Sequence["SyntaxNode"]:
        return self.literal_token,

    def span(self) -> TextSpan:
        return self.literal_token.span()
