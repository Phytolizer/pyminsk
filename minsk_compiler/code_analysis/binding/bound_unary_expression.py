from minsk_compiler.code_analysis.binding.bound_expression import BoundExpression
from minsk_compiler.code_analysis.binding.bound_node_kind import BoundNodeKind
from minsk_compiler.code_analysis.binding.bound_unary_operator import BoundUnaryOperator


class BoundUnaryExpression(BoundExpression):
    operator: BoundUnaryOperator
    operand: BoundExpression

    def __init__(self, operator: BoundUnaryOperator, operand: BoundExpression):
        self.operator = operator
        self.operand = operand

    def type(self):
        return self.operator.type

    def kind(self) -> BoundNodeKind:
        return BoundNodeKind.UNARY_EXPRESSION
