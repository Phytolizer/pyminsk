from dataclasses import dataclass
from typing import Sequence

from minsk.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_node import SyntaxNode
from minsk.code_analysis.syntax.syntax_token import SyntaxToken
from minsk.code_analysis.text_span import TextSpan


@dataclass
class AssignmentExpressionSyntax(ExpressionSyntax):
    identifier_token: SyntaxToken
    equals_token: SyntaxToken
    expression: ExpressionSyntax

    def kind(self) -> SyntaxKind:
        return SyntaxKind.ASSIGNMENT_EXPRESSION

    def children(self) -> Sequence["SyntaxNode"]:
        return self.identifier_token, self.equals_token, self.expression

    def span(self) -> TextSpan:
        return TextSpan.from_bounds(self.identifier_token.span().start,
                                    self.expression.span().end())
