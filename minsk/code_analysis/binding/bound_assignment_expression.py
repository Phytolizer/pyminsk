from dataclasses import dataclass

from minsk.code_analysis.binding.bound_expression import BoundExpression
from minsk.code_analysis.binding.bound_node_kind import BoundNodeKind
from minsk.code_analysis.variable_symbol import VariableSymbol


@dataclass
class BoundAssignmentExpression(BoundExpression):
    variable: VariableSymbol
    expression: BoundExpression

    def type(self):
        return self.variable.type

    def kind(self) -> BoundNodeKind:
        return BoundNodeKind.ASSIGNMENT_EXPRESSION
