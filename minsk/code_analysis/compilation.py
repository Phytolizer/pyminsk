from typing import Any

from minsk.code_analysis.binding.binder import Binder
from minsk.code_analysis.diagnostic_bag import DiagnosticBag
from minsk.code_analysis.evaluation_result import EvaluationResult
from minsk.code_analysis.evaluator import Evaluator
from minsk.code_analysis.syntax.syntax_tree import SyntaxTree
from minsk.code_analysis.variable_symbol import VariableSymbol


class Compilation:
    syntax: SyntaxTree

    def __init__(self, syntax: SyntaxTree):
        self.syntax = syntax

    def evaluate(self, variables: dict[VariableSymbol, Any]) -> EvaluationResult:
        binder = Binder(variables)
        bound_expression = binder.bind_expression(self.syntax.root)
        diagnostics = self.syntax.diagnostics + binder.diagnostics
        if len(diagnostics) > 0:
            return EvaluationResult(diagnostics, None)
        evaluator = Evaluator(bound_expression, variables)
        value = evaluator.evaluate()
        return EvaluationResult(DiagnosticBag(), value)
