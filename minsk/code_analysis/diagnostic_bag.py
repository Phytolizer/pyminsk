from typing import Collection, Iterator, Type

from minsk.code_analysis.diagnostic import Diagnostic
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.text_span import TextSpan
from tools.addable import Addable


class DiagnosticBag(Collection[Diagnostic], Addable):
    _diagnostics: list[Diagnostic]

    def __init__(self):
        self._diagnostics = []

    def __len__(self) -> int:
        return len(self._diagnostics)

    def __iter__(self) -> Iterator[Diagnostic]:
        return iter(self._diagnostics)

    def __contains__(self, x: object) -> bool:
        return x in self._diagnostics

    def __add__(self, other: "DiagnosticBag") -> "DiagnosticBag":
        out = DiagnosticBag()
        out._diagnostics = self._diagnostics + other._diagnostics
        return out

    def __iadd__(self, other: "DiagnosticBag"):
        self._diagnostics += other._diagnostics

    def _report(self, span: TextSpan, message: str):
        diagnostic = Diagnostic(span, message)
        self._diagnostics.append(diagnostic)

    def report_bad_character(self, span: TextSpan, char: str):
        message = f"bad character in input: '{char}'"
        self._report(span, message)

    def report_unexpected_token(self, span: TextSpan, actual_kind: SyntaxKind, expected_kind: SyntaxKind):
        message = f"unexpected token <{actual_kind}>, expected <{expected_kind}>"
        self._report(span, message)

    def report_undefined_unary_operator(self, span: TextSpan, operator_text: str, operand_type: Type):
        message = f"unary operator '{operator_text}' is not defined for type {operand_type.__name__}"
        self._report(span, message)

    def report_undefined_binary_operator(self, span: TextSpan, operator_text: str, left_type: Type, right_type: Type):
        message = (f"binary operator '{operator_text}' is not defined for types {left_type.__name__} and "
                   f"{right_type.__name__}")
        self._report(span, message)

    def report_undefined_name(self, span: TextSpan, name: str):
        message = f"variable '{name}' doesn't exist"
        self._report(span, message)
