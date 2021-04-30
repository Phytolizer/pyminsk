from typing import Any
from minsk_compiler.syntax_kind import SyntaxKind


class SyntaxToken:
    kind: SyntaxKind
    position: int
    text: str

    def __init__(self, kind: SyntaxKind, position: int, text: str, value: Any = None):
        self.kind = kind
        self.position = position
        self.text = text
        self.value = value

    def __str__(self) -> str:
        out = f"{self.kind} {self.text}"
        if self.value is not None:
            out += f" {self.value}"
        return out
