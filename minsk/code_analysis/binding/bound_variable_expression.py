from dataclasses import dataclass
from typing import Type

from minsk.code_analysis.binding.bound_expression import BoundExpression
from minsk.code_analysis.binding.bound_node_kind import BoundNodeKind
from minsk.code_analysis.variable_symbol import VariableSymbol


@dataclass
class BoundVariableExpression(BoundExpression):
    variable: VariableSymbol

    def type(self):
        return self.variable.type

    def kind(self) -> BoundNodeKind:
        return BoundNodeKind.VARIABLE_EXPRESSION
