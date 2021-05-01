from minsk_compiler.code_analysis.binding.bound_expression import BoundExpression
from minsk_compiler.code_analysis.binding.bound_node_kind import BoundNodeKind
from minsk_compiler.code_analysis.binding.bound_unary_operator_kind import BoundUnaryOperatorKind


class BoundUnaryExpression(BoundExpression):
    def __init__(self, operator_kind: BoundUnaryOperatorKind, operand: BoundExpression):
        self.operator_kind = operator_kind
        self.operand = operand

    def type(self):
        return self.operand.type()

    def kind(self) -> BoundNodeKind:
        return BoundNodeKind.UNARY_EXPRESSION
