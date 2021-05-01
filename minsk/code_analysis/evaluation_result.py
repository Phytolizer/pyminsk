from typing import Any, Collection

from minsk.code_analysis.diagnostic import Diagnostic


class EvaluationResult:
    diagnostics: Collection[Diagnostic]
    value: Any

    def __init__(self, diagnostics: Collection[Diagnostic], value: Any):
        self.diagnostics = diagnostics
        self.value = value
