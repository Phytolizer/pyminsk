from dataclasses import dataclass

from minsk.code_analysis.binding.bound_expression import BoundExpression
from minsk.code_analysis.binding.bound_node_kind import BoundNodeKind


@dataclass
class BoundAssignmentExpression(BoundExpression):
    name: str
    expression: BoundExpression

    def type(self):
        return self.expression.type()

    def kind(self) -> BoundNodeKind:
        return BoundNodeKind.ASSIGNMENT_EXPRESSION
