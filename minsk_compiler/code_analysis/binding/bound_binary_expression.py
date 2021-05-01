from minsk_compiler.code_analysis.binding.bound_binary_operator_kind import BoundBinaryOperatorKind
from minsk_compiler.code_analysis.binding.bound_expression import BoundExpression
from minsk_compiler.code_analysis.binding.bound_node_kind import BoundNodeKind


class BoundBinaryExpression(BoundExpression):
    def __init__(self, left: BoundExpression, operator_kind: BoundBinaryOperatorKind, right: BoundExpression):
        self.left = left
        self.operator_kind = operator_kind
        self.right = right

    def type(self):
        return self.left.type()

    def kind(self) -> BoundNodeKind:
        return BoundNodeKind.BINARY_EXPRESSION
