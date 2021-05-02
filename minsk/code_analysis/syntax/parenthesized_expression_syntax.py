from dataclasses import dataclass
from typing import Sequence

from minsk.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_node import SyntaxNode
from minsk.code_analysis.syntax.syntax_token import SyntaxToken
from minsk.code_analysis.text.text_span import TextSpan


@dataclass
class ParenthesizedExpressionSyntax(ExpressionSyntax):
    open_parenthesis_token: SyntaxToken
    expression: ExpressionSyntax
    close_parenthesis_token: SyntaxToken

    def kind(self) -> SyntaxKind:
        return SyntaxKind.PARENTHESIZED_EXPRESSION

    def children(self) -> Sequence["SyntaxNode"]:
        return self.open_parenthesis_token, self.expression, self.close_parenthesis_token

    def span(self) -> TextSpan:
        return TextSpan.from_bounds(self.open_parenthesis_token.span().start,
                                    self.close_parenthesis_token.span().end())
