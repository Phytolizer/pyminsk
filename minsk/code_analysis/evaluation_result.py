from typing import Tuple, Any


class EvaluationResult:
    diagnostics: Tuple[str, ...]
    value: Any

    def __init__(self, diagnostics: Tuple[str, ...], value: Any):
        self.diagnostics = diagnostics
        self.value = value
