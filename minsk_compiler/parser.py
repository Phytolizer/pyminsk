from minsk_compiler.syntax_tree import SyntaxTree
from minsk_compiler.expression_syntax import ExpressionSyntax
from minsk_compiler.binary_expression_syntax import BinaryExpressionSyntax
from minsk_compiler.literal_expression_syntax import LiteralExpressionSyntax
from minsk_compiler.syntax_token import SyntaxToken
from typing import List, Tuple
from minsk_compiler.syntax_kind import SyntaxKind
from minsk_compiler.lexer import Lexer


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
            if token.kind() not in (SyntaxKind.BAD_TOKEN, SyntaxKind.WHITESPACE_TOKEN):
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

    def parse(self) -> SyntaxTree:
        expression = self._parse_expression()
        end_of_file_token = self._match_token(SyntaxKind.END_OF_FILE_TOKEN)
        return SyntaxTree(self.diagnostics, expression, end_of_file_token)

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
        literal_token = self._match_token(SyntaxKind.NUMBER_TOKEN)
        return LiteralExpressionSyntax(literal_token)
