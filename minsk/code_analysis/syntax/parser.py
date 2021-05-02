from typing import Sequence

from minsk.code_analysis.diagnostic_bag import DiagnosticBag
from minsk.code_analysis.syntax.assignment_expression_syntax import AssignmentExpressionSyntax
from minsk.code_analysis.syntax.binary_expression_syntax import BinaryExpressionSyntax
from minsk.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk.code_analysis.syntax.lexer import Lexer
from minsk.code_analysis.syntax.literal_expression_syntax import LiteralExpressionSyntax
from minsk.code_analysis.syntax.name_expression_syntax import NameExpressionSyntax
from minsk.code_analysis.syntax.parenthesized_expression_syntax import ParenthesizedExpressionSyntax
from minsk.code_analysis.syntax.syntax_facts import get_unary_operator_precedence, get_binary_operator_precedence
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_token import SyntaxToken
from minsk.code_analysis.syntax.unary_expression_syntax import UnaryExpressionSyntax


class Parser:
    _position: int
    _tokens: Sequence[SyntaxToken]
    diagnostics: DiagnosticBag

    def __init__(self, text: str):
        lexer = Lexer(text)
        tokens: list[SyntaxToken] = []
        while True:
            token = lexer.lex()
            if token.kind() not in (
                    SyntaxKind.BAD_TOKEN, SyntaxKind.WHITESPACE_TOKEN):
                tokens.append(token)
            if token.kind() == SyntaxKind.END_OF_FILE_TOKEN:
                break

        self._position = 0
        self._tokens = tokens
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

        self.diagnostics.report_unexpected_token(self._current().span(), self._current().kind(), kind)
        return SyntaxToken(kind, self._current().position, "")

    def parse(self) -> tuple[DiagnosticBag, ExpressionSyntax, SyntaxToken]:
        expression = self._parse_expression()
        end_of_file_token = self._match_token(SyntaxKind.END_OF_FILE_TOKEN)
        return self.diagnostics, expression, end_of_file_token

    def _parse_expression(self) -> ExpressionSyntax:
        return self._parse_assignment_expression()

    def _parse_assignment_expression(self) -> ExpressionSyntax:
        if self._peek(0).kind() == SyntaxKind.IDENTIFIER_TOKEN and self._peek(1).kind() == SyntaxKind.EQUALS_TOKEN:
            identifier_token = self._next_token()
            operator_token = self._next_token()
            right = self._parse_assignment_expression()
            return AssignmentExpressionSyntax(identifier_token, operator_token, right)

        return self._parse_binary_expression()

    def _parse_binary_expression(self, parent_precedence: int = 0) -> ExpressionSyntax:
        unary_operator_precedence = get_unary_operator_precedence(self._current().kind())
        left: ExpressionSyntax
        if unary_operator_precedence != 0 and unary_operator_precedence >= parent_precedence:
            operator_token = self._next_token()
            operand = self._parse_binary_expression(unary_operator_precedence)
            left = UnaryExpressionSyntax(operator_token, operand)
        else:
            left = self._parse_primary_expression()
        while True:
            precedence = get_binary_operator_precedence(self._current().kind())
            if precedence == 0 or precedence <= parent_precedence:
                break

            operator_token = self._next_token()
            right = self._parse_binary_expression(precedence)
            left = BinaryExpressionSyntax(left, operator_token, right)

        return left

    def _parse_primary_expression(self) -> ExpressionSyntax:
        if self._current().kind() == SyntaxKind.OPEN_PARENTHESIS_TOKEN:
            return self._parse_parenthesized_expression()
        elif self._current().kind() in (SyntaxKind.FALSE_KEYWORD, SyntaxKind.TRUE_KEYWORD):
            return self._parse_boolean_literal()
        elif self._current().kind() == SyntaxKind.IDENTIFIER_TOKEN:
            return self._parse_name_expression()
        else:
            return self._parse_number_literal()

    def _parse_parenthesized_expression(self):
        left = self._match_token(SyntaxKind.OPEN_PARENTHESIS_TOKEN)
        expression = self._parse_expression()
        right = self._match_token(SyntaxKind.CLOSE_PARENTHESIS_TOKEN)
        return ParenthesizedExpressionSyntax(left, expression, right)

    def _parse_number_literal(self):
        number_token = self._match_token(SyntaxKind.NUMBER_TOKEN)
        return LiteralExpressionSyntax(number_token)

    def _parse_boolean_literal(self):
        is_true = self._current().kind() == SyntaxKind.TRUE_KEYWORD
        if is_true:
            keyword_token = self._match_token(SyntaxKind.TRUE_KEYWORD)
        else:
            keyword_token = self._match_token(SyntaxKind.FALSE_KEYWORD)
        return LiteralExpressionSyntax(keyword_token, is_true)

    def _parse_name_expression(self):
        identifier_token = self._match_token(SyntaxKind.IDENTIFIER_TOKEN)
        return NameExpressionSyntax(identifier_token)
