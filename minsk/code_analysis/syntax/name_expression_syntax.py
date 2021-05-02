from typing import Sequence

from minsk.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_node import SyntaxNode
from minsk.code_analysis.syntax.syntax_token import SyntaxToken
from minsk.code_analysis.text.text_span import TextSpan


class NameExpressionSyntax(ExpressionSyntax):
    identifier_token: SyntaxToken

    def __init__(self, identifier_token: SyntaxToken):
        self.identifier_token = identifier_token

    def kind(self) -> SyntaxKind:
        return SyntaxKind.NAME_EXPRESSION

    def children(self) -> Sequence["SyntaxNode"]:
        return self.identifier_token,

    def span(self) -> TextSpan:
        return self.identifier_token.span()
