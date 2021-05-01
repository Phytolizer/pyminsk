from typing import List, Tuple

from minsk_compiler.code_analysis.lexer import Lexer
from minsk_compiler.code_analysis.syntax.binary_expression_syntax import BinaryExpressionSyntax
from minsk_compiler.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk_compiler.code_analysis.syntax.literal_expression_syntax import LiteralExpressionSyntax
from minsk_compiler.code_analysis.syntax.parenthesized_expression_syntax import ParenthesizedExpressionSyntax
from minsk_compiler.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk_compiler.code_analysis.syntax.syntax_token import SyntaxToken


class Parser:
    _position: int
    _tokens: Tuple[SyntaxToken, ...]
    diagnostics: List[str]

    def __init__(self, text: str):
        lexer = Lexer(text)
        token = None
        tokens: List[SyntaxToken] = []
        while True:
            token = lexer.next_token()
            if token.kind() not in (
                    SyntaxKind.BAD_TOKEN, SyntaxKind.WHITESPACE_TOKEN):
                tokens.append(token)
            if token.kind() == SyntaxKind.END_OF_FILE_TOKEN:
                break

        self._position = 0
        self._tokens = tuple(tokens)
        self.diagnostics = lexer.diagnostics

    def _peek(self, offset: int) -> SyntaxToken:
        index = self._position + offset
        if index >= len(self._tokens):
            return self._tokens[-1]
        return self._tokens[index]

    def _current(self) -> SyntaxToken:
        return self._peek(0)

    def _next_token(self) -> SyntaxToken:
        current = self._current()
        self._position += 1
        return current

    def _match_token(self, kind: SyntaxKind) -> SyntaxToken:
        if self._current().kind() == kind:
            return self._next_token()

        self.diagnostics.append(
            f"ERROR: Unexpected token <{self._current().kind()}>, expected <{kind}>"
        )
        return SyntaxToken(kind, self._current().position, "")

    def parse(self) -> Tuple[List[str], ExpressionSyntax, SyntaxToken]:
        expression = self._parse_expression()
        end_of_file_token = self._match_token(SyntaxKind.END_OF_FILE_TOKEN)
        return (self.diagnostics, expression, end_of_file_token)

    def _parse_expression(self) -> ExpressionSyntax:
        return self._parse_term()

    def _parse_term(self) -> ExpressionSyntax:
        left = self._parse_factor()

        while (
                self._current().kind() == SyntaxKind.PLUS_TOKEN
                or self._current().kind() == SyntaxKind.MINUS_TOKEN
        ):
            operator_token = self._next_token()
            right = self._parse_factor()
            left = BinaryExpressionSyntax(left, operator_token, right)

        return left

    def _parse_factor(self) -> ExpressionSyntax:
        left = self._parse_primary_expression()

        while (
                self._current().kind() == SyntaxKind.STAR_TOKEN
                or self._current().kind() == SyntaxKind.SLASH_TOKEN
        ):
            operator_token = self._next_token()
            right = self._parse_primary_expression()
            left = BinaryExpressionSyntax(left, operator_token, right)

        return left

    def _parse_primary_expression(self) -> ExpressionSyntax:
        if self._current().kind() == SyntaxKind.OPEN_PARENTHESIS_TOKEN:
            left = self._next_token()
            expression = self._parse_expression()
            right = self._match_token(SyntaxKind.CLOSE_PARENTHESIS_TOKEN)
            return ParenthesizedExpressionSyntax(left, expression, right)
        literal_token = self._match_token(SyntaxKind.NUMBER_TOKEN)
        return LiteralExpressionSyntax(literal_token)
