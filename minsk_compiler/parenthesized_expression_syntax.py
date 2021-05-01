from typing import Iterable
from minsk_compiler.expression_syntax import ExpressionSyntax
from minsk_compiler.syntax_token import SyntaxToken
from minsk_compiler.syntax_kind import SyntaxKind
from minsk_compiler.syntax_node import SyntaxNode


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

    def children(self) -> Iterable["SyntaxNode"]:
        return (
            self.open_parenthesis_token,
            self.expression,
            self.close_parenthesis_token,
        )
