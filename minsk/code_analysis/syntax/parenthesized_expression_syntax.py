from typing import Sequence

from minsk.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_node import SyntaxNode
from minsk.code_analysis.syntax.syntax_token import SyntaxToken


class ParenthesizedExpressionSyntax(ExpressionSyntax):
    open_parenthesis_token: SyntaxToken
    expression: ExpressionSyntax
    close_parenthesis_token: SyntaxToken

    def __init__(
            self,
            open_parenthesis_token: SyntaxToken,
            expression: ExpressionSyntax,
            close_parenthesis_token: SyntaxToken,
    ):
        self.open_parenthesis_token = open_parenthesis_token
        self.expression = expression
        self.close_parenthesis_token = close_parenthesis_token

    def kind(self) -> SyntaxKind:
        return SyntaxKind.PARENTHESIZED_EXPRESSION

    def children(self) -> Sequence["SyntaxNode"]:
        return (
            self.open_parenthesis_token,
            self.expression,
            self.close_parenthesis_token,
        )
