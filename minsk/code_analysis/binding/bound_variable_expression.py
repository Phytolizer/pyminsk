from dataclasses import dataclass
from typing import Type

from minsk.code_analysis.binding.bound_expression import BoundExpression
from minsk.code_analysis.binding.bound_node_kind import BoundNodeKind


@dataclass
class BoundVariableExpression(BoundExpression):
    name: str
    ty: Type

    def type(self):
        return self.ty

    def kind(self) -> BoundNodeKind:
        return BoundNodeKind.VARIABLE_EXPRESSION
