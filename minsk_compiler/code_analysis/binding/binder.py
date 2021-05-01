from typing import cast, List, Optional

from minsk_compiler.code_analysis.binding.bound_binary_expression import BoundBinaryExpression
from minsk_compiler.code_analysis.binding.bound_binary_operator import BoundBinaryOperator
from minsk_compiler.code_analysis.binding.bound_binary_operator_kind import BoundBinaryOperatorKind
from minsk_compiler.code_analysis.binding.bound_expression import BoundExpression
from minsk_compiler.code_analysis.binding.bound_literal_expression import BoundLiteralExpression
from minsk_compiler.code_analysis.binding.bound_unary_expression import BoundUnaryExpression
from minsk_compiler.code_analysis.binding.bound_unary_operator import BoundUnaryOperator
from minsk_compiler.code_analysis.binding.bound_unary_operator_kind import BoundUnaryOperatorKind
from minsk_compiler.code_analysis.syntax.binary_expression_syntax import BinaryExpressionSyntax
from minsk_compiler.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk_compiler.code_analysis.syntax.literal_expression_syntax import LiteralExpressionSyntax
from minsk_compiler.code_analysis.syntax.parenthesized_expression_syntax import ParenthesizedExpressionSyntax
from minsk_compiler.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk_compiler.code_analysis.syntax.unary_expression_syntax import UnaryExpressionSyntax


class Binder:
    diagnostics: List[str]

    def __init__(self):
        self.diagnostics = []

    def bind_expression(self, syntax: ExpressionSyntax) -> BoundExpression:
        if syntax.kind() == SyntaxKind.LITERAL_EXPRESSION:
            return self._bind_literal_expression(cast(LiteralExpressionSyntax, syntax))
        elif syntax.kind() == SyntaxKind.UNARY_EXPRESSION:
            return self._bind_unary_expression(cast(UnaryExpressionSyntax, syntax))
        elif syntax.kind() == SyntaxKind.BINARY_EXPRESSION:
            return self._bind_binary_expression(cast(BinaryExpressionSyntax, syntax))
        elif syntax.kind() == SyntaxKind.PARENTHESIZED_EXPRESSION:
            return self._bind_parenthesized_expression(cast(ParenthesizedExpressionSyntax, syntax))
        else:
            raise Exception(f"unexpected syntax {syntax.kind()}")

    def _bind_literal_expression(self, syntax: LiteralExpressionSyntax) -> BoundExpression:
        value = syntax.value
        if value is None:
            value = 0
        return BoundLiteralExpression(value)

    def _bind_unary_expression(self, syntax: UnaryExpressionSyntax) -> BoundExpression:
        bound_operand = self.bind_expression(syntax.operand)
        bound_operator_kind = BoundUnaryOperator.bind(syntax.operator_token.kind(), bound_operand.type())
        if bound_operator_kind is None:
            self.diagnostics.append(
                f"Unary operator '{syntax.operator_token.text}' is not defined for type {bound_operand.type()}")
            return bound_operand
        return BoundUnaryExpression(bound_operator_kind, bound_operand)

    def _bind_binary_expression(self, syntax: BinaryExpressionSyntax) -> BoundExpression:
        bound_left = self.bind_expression(syntax.left)
        bound_right = self.bind_expression(syntax.right)
        bound_operator_kind = BoundBinaryOperator.bind(syntax.operator_token.kind(), bound_left.type(),
                                                       bound_right.type())
        if bound_operator_kind is None:
            self.diagnostics.append(
                f"Binary operator '{syntax.operator_token.text}' is not defined for types {bound_left.type()} "
                f"and {bound_right.type()}")
            return bound_left
        return BoundBinaryExpression(bound_left, bound_operator_kind, bound_right)

    def _bind_parenthesized_expression(self, syntax: ParenthesizedExpressionSyntax) -> BoundExpression:
        return self.bind_expression(syntax.expression)
