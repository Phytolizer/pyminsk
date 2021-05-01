from minsk.code_analysis.binding.binder import Binder
from minsk.code_analysis.evaluation_result import EvaluationResult
from minsk.code_analysis.evaluator import Evaluator
from minsk.code_analysis.syntax.syntax_tree import SyntaxTree


class Compilation:
    syntax: SyntaxTree

    def __init__(self, syntax: SyntaxTree):
        self.syntax = syntax

    def evaluate(self) -> EvaluationResult:
        binder = Binder()
        bound_expression = binder.bind_expression(self.syntax.root)
        diagnostics = self.syntax.diagnostics + tuple(binder.diagnostics)
        if len(diagnostics) > 0:
            return EvaluationResult(diagnostics, None)
        evaluator = Evaluator(bound_expression)
        value = evaluator.evaluate()
        return EvaluationResult((), value)
