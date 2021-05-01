from minsk.code_analysis.binding.bound_binary_operator import BoundBinaryOperator
from minsk.code_analysis.binding.bound_expression import BoundExpression
from minsk.code_analysis.binding.bound_node_kind import BoundNodeKind


class BoundBinaryExpression(BoundExpression):
    left: BoundExpression
    operator: BoundBinaryOperator
    right: BoundExpression

    def __init__(self, left: BoundExpression, operator: BoundBinaryOperator, right: BoundExpression):
        self.left = left
        self.operator = operator
        self.right = right

    def type(self):
        return self.operator.type

    def kind(self) -> BoundNodeKind:
        return BoundNodeKind.BINARY_EXPRESSION
