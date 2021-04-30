from minsk_compiler.expression_syntax import ExpressionSyntax
from minsk_compiler.syntax_token import SyntaxToken
from minsk_compiler.syntax_kind import SyntaxKind
from minsk_compiler.syntax_node import SyntaxNode
from typing import Iterable


class BinaryExpressionSyntax(ExpressionSyntax):
    left: ExpressionSyntax
    operator_token: SyntaxToken
    right: ExpressionSyntax

    def __init__(self, left: ExpressionSyntax, operator_token: SyntaxToken, right: ExpressionSyntax):
        self.left = left
        self.operator_token = operator_token
        self.right = right

    def kind(self) -> SyntaxKind:
        return SyntaxKind.BINARY_EXPRESSION

    def children(self) -> Iterable["SyntaxNode"]:
        return (self.left, self.operator_token, self.right)
