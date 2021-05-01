from typing import Sequence

from minsk.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_node import SyntaxNode
from minsk.code_analysis.syntax.syntax_token import SyntaxToken


class BinaryExpressionSyntax(ExpressionSyntax):
    left: ExpressionSyntax
    operator_token: SyntaxToken
    right: ExpressionSyntax

    def __init__(self, left: ExpressionSyntax, operator_token: SyntaxToken,
                 right: ExpressionSyntax):
        self.left = left
        self.operator_token = operator_token
        self.right = right

    def kind(self) -> SyntaxKind:
        return SyntaxKind.BINARY_EXPRESSION

    def children(self) -> Sequence["SyntaxNode"]:
        return self.left, self.operator_token, self.right
