from typing import Any

from minsk.code_analysis.binding.bound_expression import BoundExpression
from minsk.code_analysis.binding.bound_node_kind import BoundNodeKind


class BoundLiteralExpression(BoundExpression):
    value: Any

    def __init__(self, value: Any):
        self.value = value

    def type(self):
        return type(self.value)

    def kind(self) -> BoundNodeKind:
        return BoundNodeKind.LITERAL_EXPRESSION
