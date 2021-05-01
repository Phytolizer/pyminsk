from typing import cast, Any

from minsk.code_analysis.binding.bound_assignment_expression import BoundAssignmentExpression
from minsk.code_analysis.binding.bound_binary_expression import BoundBinaryExpression
from minsk.code_analysis.binding.bound_binary_operator import BoundBinaryOperator
from minsk.code_analysis.binding.bound_expression import BoundExpression
from minsk.code_analysis.binding.bound_literal_expression import BoundLiteralExpression
from minsk.code_analysis.binding.bound_unary_expression import BoundUnaryExpression
from minsk.code_analysis.binding.bound_unary_operator import BoundUnaryOperator
from minsk.code_analysis.binding.bound_variable_expression import BoundVariableExpression
from minsk.code_analysis.diagnostic_bag import DiagnosticBag
from minsk.code_analysis.syntax.assignment_expression_syntax import AssignmentExpressionSyntax
from minsk.code_analysis.syntax.binary_expression_syntax import BinaryExpressionSyntax
from minsk.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk.code_analysis.syntax.literal_expression_syntax import LiteralExpressionSyntax
from minsk.code_analysis.syntax.name_expression_syntax import NameExpressionSyntax
from minsk.code_analysis.syntax.parenthesized_expression_syntax import ParenthesizedExpressionSyntax
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.unary_expression_syntax import UnaryExpressionSyntax
from minsk.code_analysis.variable_symbol import VariableSymbol


class Binder:
    _variables: dict[VariableSymbol, Any]
    diagnostics: DiagnosticBag

    def __init__(self, variables: dict[VariableSymbol, Any]):
        self._variables = variables
        self.diagnostics = DiagnosticBag()

    def bind_expression(self, syntax: ExpressionSyntax) -> BoundExpression:
        if syntax.kind() == SyntaxKind.LITERAL_EXPRESSION:
            return self._bind_literal_expression(cast(LiteralExpressionSyntax, syntax))
        elif syntax.kind() == SyntaxKind.UNARY_EXPRESSION:
            return self._bind_unary_expression(cast(UnaryExpressionSyntax, syntax))
        elif syntax.kind() == SyntaxKind.BINARY_EXPRESSION:
            return self._bind_binary_expression(cast(BinaryExpressionSyntax, syntax))
        elif syntax.kind() == SyntaxKind.PARENTHESIZED_EXPRESSION:
            return self._bind_parenthesized_expression(cast(ParenthesizedExpressionSyntax, syntax))
        elif syntax.kind() == SyntaxKind.NAME_EXPRESSION:
            return self._bind_name_expression(cast(NameExpressionSyntax, syntax))
        elif syntax.kind() == SyntaxKind.ASSIGNMENT_EXPRESSION:
            return self._bind_assignment_expression(cast(AssignmentExpressionSyntax, syntax))
        else:
            raise Exception(f"unexpected syntax {syntax.kind()}")

    def _bind_literal_expression(self, syntax: LiteralExpressionSyntax) -> BoundExpression:
        value = syntax.value
        if value is None:
            value = 0
        return BoundLiteralExpression(value)

    def _bind_unary_expression(self, syntax: UnaryExpressionSyntax) -> BoundExpression:
        bound_operand = self.bind_expression(syntax.operand)
        bound_operator = BoundUnaryOperator.bind(syntax.operator_token.kind(), bound_operand.type())
        if bound_operator is None:
            self.diagnostics.report_undefined_unary_operator(syntax.operator_token.span, syntax.operator_token.text,
                                                             bound_operand.type())
            return bound_operand
        return BoundUnaryExpression(bound_operator, bound_operand)

    def _bind_binary_expression(self, syntax: BinaryExpressionSyntax) -> BoundExpression:
        bound_left = self.bind_expression(syntax.left)
        bound_right = self.bind_expression(syntax.right)
        bound_operator = BoundBinaryOperator.bind(syntax.operator_token.kind(), bound_left.type(),
                                                  bound_right.type())
        if bound_operator is None:
            self.diagnostics.report_undefined_binary_operator(syntax.operator_token.span, syntax.operator_token.text,
                                                              bound_left.type(), bound_right.type())
            return bound_left
        return BoundBinaryExpression(bound_left, bound_operator, bound_right)

    def _bind_parenthesized_expression(self, syntax: ParenthesizedExpressionSyntax) -> BoundExpression:
        return self.bind_expression(syntax.expression)

    def _bind_name_expression(self, syntax: NameExpressionSyntax) -> BoundExpression:
        name = syntax.identifier_token.text
        variable = next(filter(lambda v: v.name == name, self._variables.keys()), None)
        if variable is None:
            self.diagnostics.report_undefined_name(syntax.identifier_token.span, name)
            return BoundLiteralExpression(0)

        return BoundVariableExpression(variable)

    def _bind_assignment_expression(self, syntax: AssignmentExpressionSyntax) -> BoundExpression:
        name = syntax.identifier_token.text
        bound_expression = self.bind_expression(syntax.expression)

        existing_variable = next(filter(lambda v: v.name == name, self._variables.keys()), None)
        if existing_variable is not None:
            del self._variables[existing_variable]
        variable = VariableSymbol(name, bound_expression.type())
        self._variables[variable] = None

        return BoundAssignmentExpression(variable, bound_expression)
