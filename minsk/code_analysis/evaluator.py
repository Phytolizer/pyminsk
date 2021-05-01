from typing import cast, Any

from minsk.code_analysis.binding.bound_assignment_expression import BoundAssignmentExpression
from minsk.code_analysis.binding.bound_binary_expression import BoundBinaryExpression
from minsk.code_analysis.binding.bound_binary_operator_kind import BoundBinaryOperatorKind
from minsk.code_analysis.binding.bound_expression import BoundExpression
from minsk.code_analysis.binding.bound_literal_expression import BoundLiteralExpression
from minsk.code_analysis.binding.bound_node_kind import BoundNodeKind
from minsk.code_analysis.binding.bound_unary_expression import BoundUnaryExpression
from minsk.code_analysis.binding.bound_unary_operator_kind import BoundUnaryOperatorKind
from minsk.code_analysis.binding.bound_variable_expression import BoundVariableExpression
from minsk.code_analysis.variable_symbol import VariableSymbol


class Evaluator:
    _variables: dict[VariableSymbol, Any]
    _root: BoundExpression

    def __init__(self, root: BoundExpression, variables: dict[VariableSymbol, Any]):
        self._variables = variables
        self._root = root

    def evaluate(self) -> Any:
        return self._evaluate_expression(self._root)

    def _evaluate_expression(self, root: BoundExpression) -> Any:
        if root.kind() == BoundNodeKind.LITERAL_EXPRESSION:
            root = cast(BoundLiteralExpression, root)
            return root.value
        elif root.kind() == BoundNodeKind.VARIABLE_EXPRESSION:
            root = cast(BoundVariableExpression, root)
            return self._variables[root.variable]
        elif root.kind() == BoundNodeKind.ASSIGNMENT_EXPRESSION:
            root = cast(BoundAssignmentExpression, root)
            value = self._evaluate_expression(root.expression)
            self._variables[root.variable] = value
            return value
        elif root.kind() == BoundNodeKind.UNARY_EXPRESSION:
            root = cast(BoundUnaryExpression, root)
            operand = self._evaluate_expression(root.operand)

            if root.operator.kind == BoundUnaryOperatorKind.IDENTITY:
                return operand
            elif root.operator.kind == BoundUnaryOperatorKind.NEGATION:
                return -operand
            elif root.operator.kind == BoundUnaryOperatorKind.LOGICAL_NEGATION:
                return not operand
            else:
                raise Exception(f"unexpected unary operator {root.operator.kind}")

        elif root.kind() == BoundNodeKind.BINARY_EXPRESSION:
            root = cast(BoundBinaryExpression, root)
            left = self._evaluate_expression(root.left)
            right = self._evaluate_expression(root.right)

            if root.operator.kind == BoundBinaryOperatorKind.ADDITION:
                return left + right
            elif root.operator.kind == BoundBinaryOperatorKind.SUBTRACTION:
                return left - right
            elif root.operator.kind == BoundBinaryOperatorKind.MULTIPLICATION:
                return left * right
            elif root.operator.kind == BoundBinaryOperatorKind.DIVISION:
                return left // right
            elif root.operator.kind == BoundBinaryOperatorKind.LOGICAL_AND:
                return left and right
            elif root.operator.kind == BoundBinaryOperatorKind.LOGICAL_OR:
                return left or right
            elif root.operator.kind == BoundBinaryOperatorKind.EQUALITY:
                return left == right
            elif root.operator.kind == BoundBinaryOperatorKind.INEQUALITY:
                return left != right
            else:
                raise Exception(f"unexpected binary operator {root.operator}")

        else:
            raise Exception(f"unexpected node {root.kind()}")
