from dataclasses import dataclass
from typing import Sequence

from minsk.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_node import SyntaxNode
from minsk.code_analysis.syntax.syntax_token import SyntaxToken
from minsk.code_analysis.text_span import TextSpan


@dataclass
class UnaryExpressionSyntax(ExpressionSyntax):
    operator_token: SyntaxToken
    operand: ExpressionSyntax

    def kind(self) -> SyntaxKind:
        return SyntaxKind.UNARY_EXPRESSION

    def children(self) -> Sequence["SyntaxNode"]:
        return self.operator_token, self.operand

    def span(self) -> TextSpan:
        return TextSpan.from_bounds(self.operator_token.span().start, self.operand.span().end().start)
