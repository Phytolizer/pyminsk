from collections import Sequence

from minsk.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_node import SyntaxNode
from minsk.code_analysis.syntax.syntax_token import SyntaxToken


class UnaryExpressionSyntax(ExpressionSyntax):
    def __init__(self, operator_token: SyntaxToken, operand: ExpressionSyntax):
        self.operator_token = operator_token
        self.operand = operand

    def kind(self) -> SyntaxKind:
        return SyntaxKind.UNARY_EXPRESSION

    def children(self) -> Sequence["SyntaxNode"]:
        return self.operator_token, self.operand
