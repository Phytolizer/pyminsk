from typing import cast, Any

from minsk_compiler.code_analysis.binding.bound_binary_expression import BoundBinaryExpression
from minsk_compiler.code_analysis.binding.bound_binary_operator_kind import BoundBinaryOperatorKind
from minsk_compiler.code_analysis.binding.bound_expression import BoundExpression
from minsk_compiler.code_analysis.binding.bound_literal_expression import BoundLiteralExpression
from minsk_compiler.code_analysis.binding.bound_node_kind import BoundNodeKind
from minsk_compiler.code_analysis.binding.bound_unary_expression import BoundUnaryExpression
from minsk_compiler.code_analysis.binding.bound_unary_operator_kind import BoundUnaryOperatorKind


class Evaluator:
    _root: BoundExpression

    def __init__(self, root: BoundExpression):
        self._root = root

    def evaluate(self) -> Any:
        return self._evaluate_expression(self._root)

    def _evaluate_expression(self, root: BoundExpression) -> Any:
        if root.kind() == BoundNodeKind.LITERAL_EXPRESSION:
            root = cast(BoundLiteralExpression, root)
            return root.value
        elif root.kind() == BoundNodeKind.UNARY_EXPRESSION:
            root = cast(BoundUnaryExpression, root)
            operand = self._evaluate_expression(root.operand)
            assert isinstance(operand, int)

            if root.operator_kind == BoundUnaryOperatorKind.IDENTITY:
                return operand
            elif root.operator_kind == BoundUnaryOperatorKind.NEGATION:
                return -operand
            else:
                raise Exception(f"unexpected unary operator {root.operator_kind}")

        elif root.kind() == BoundNodeKind.BINARY_EXPRESSION:
            root = cast(BoundBinaryExpression, root)
            left = self._evaluate_expression(root.left)
            right = self._evaluate_expression(root.right)
            assert isinstance(left, int)
            assert isinstance(right, int)

            if root.operator_kind == BoundBinaryOperatorKind.ADDITION:
                return left + right
            elif root.operator_kind == BoundBinaryOperatorKind.SUBTRACTION:
                return left - right
            elif root.operator_kind == BoundBinaryOperatorKind.MULTIPLICATION:
                return left * right
            elif root.operator_kind == BoundBinaryOperatorKind.DIVISION:
                return left // right
            else:
                raise Exception(f"unexpected binary operator {root.operator_kind}")

        else:
            raise Exception(f"unexpected node {root.kind()}")
